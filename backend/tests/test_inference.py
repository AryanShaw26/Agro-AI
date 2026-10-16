import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.models.db_models import Disease
from app.ml.class_map import CLASS_NAMES, parse_raw_class
from app.ml.model_registry import model_registry

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["classes_supported"] == 38
    assert data["gradcam_integrated"] is True
    assert data["genai_enabled"] is False

def test_model_metadata_endpoint():
    response = client.get("/api/v1/model")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert "EfficientNetV2-S" in data["model_name"]
    assert data["metadata"]["num_classes"] == 38
    assert len(data["metadata"]["class_names"]) == 38

def test_database_seeded_38_classes():
    db = SessionLocal()
    count = db.query(Disease).count()
    db.close()
    assert count == 38, f"Expected 38 seeded classes in DB, found {count}"

def test_class_names_count():
    assert len(CLASS_NAMES) == 38

def test_parse_raw_class():
    parsed = parse_raw_class("Tomato___Early_blight")
    assert parsed["crop"] == "Tomato"
    assert parsed["disease"] == "Early Blight"
    assert parsed["is_healthy"] is False

    parsed_healthy = parse_raw_class("Apple___healthy")
    assert parsed_healthy["crop"] == "Apple"
    assert parsed_healthy["disease"] == "Healthy"
    assert parsed_healthy["is_healthy"] is True

def test_predict_endpoint_valid_image():
    # Create test 384x384 RGB image matching V2-S input size
    img = Image.new("RGB", (384, 384), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/api/v1/predict",
        files={"image": ("test_leaf.jpg", buf, "image/jpeg")},
        data={"include_gradcam": "true"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction_id" in data
    assert "crop" in data
    assert "disease" in data
    assert "confidence" in data
    assert "confidence_state" in data
    assert len(data["top_predictions"]) == 3
    assert data["knowledge"]["available"] is True
    
    # Check Grad-CAM integration
    assert data["gradcam"] is not None
    assert data["gradcam"]["available"] is True
    pred_id = data["prediction_id"]

    # Test Grad-CAM streaming endpoints
    overlay_res = client.get(f"/api/v1/predictions/{pred_id}/gradcam")
    assert overlay_res.status_code == 200
    assert overlay_res.headers["content-type"] == "image/jpeg"

    heatmap_res = client.get(f"/api/v1/predictions/{pred_id}/gradcam/heatmap")
    assert heatmap_res.status_code == 200
    assert heatmap_res.headers["content-type"] == "image/jpeg"

def test_predict_endpoint_invalid_format():
    buf = io.BytesIO(b"fake text content")
    response = client.post(
        "/api/v1/predict",
        files={"image": ("test.txt", buf, "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_diseases_list_endpoint():
    response = client.get("/api/v1/diseases")
    assert response.status_code == 200
    diseases = response.json()
    assert len(diseases) == 38

def test_diseases_filter_by_crop():
    response = client.get("/api/v1/diseases?crop=Tomato")
    assert response.status_code == 200
    diseases = response.json()
    assert len(diseases) == 10
    for d in diseases:
        assert d["crop"] == "Tomato"
