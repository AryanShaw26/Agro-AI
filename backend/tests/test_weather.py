import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.services.weather_impact_service import weather_impact_service

client = TestClient(app)

def test_weather_missing_parameters():
    """Requesting weather without lat/lon or city must return 400."""
    response = client.get("/api/v1/weather")
    assert response.status_code == 400
    assert "Missing location parameter" in response.json()["detail"]

def test_weather_by_coordinates():
    """Coordinates lookup returns normalized weather and deterministic agricultural advisory."""
    # Kolkata coordinates
    response = client.get("/api/v1/weather?lat=22.5726&lon=88.3639")
    assert response.status_code == 200
    data = response.json()

    # Core weather assertions
    assert "location" in data
    assert data["location"]["name"] != ""
    assert isinstance(data["temperature"], (int, float))
    assert isinstance(data["humidity"], int)
    assert 0 <= data["humidity"] <= 100
    assert isinstance(data["wind_speed"], (int, float))
    assert isinstance(data["condition"], str)
    assert isinstance(data["description"], str)
    assert isinstance(data["icon"], str)
    assert isinstance(data["observed_at"], int)

    # Advisory assertions
    assert "advisory" in data
    if data["advisory"] is not None:
        adv = data["advisory"]
        assert adv["severity"] in ["LOW", "MODERATE", "HIGH"]
        assert isinstance(adv["weather_hazard"], str)
        assert isinstance(adv["explanation"], str)
        assert isinstance(adv["possible_crop_consequence"], str)
        assert isinstance(adv["actions"], list)
        assert len(adv["actions"]) > 0
        assert isinstance(adv["limitations"], str) and len(adv["limitations"]) > 0
        assert isinstance(adv["source"], str)

def test_weather_by_city_fallback():
    """Manual city query returns valid weather response."""
    response = client.get("/api/v1/weather?city=London,GB")
    assert response.status_code == 200
    data = response.json()
    assert "London" in data["location"]["name"] or data["location"]["country"] == "GB"

def test_weather_cache_reuse():
    """Consecutive queries for same coordinates return cached response."""
    res1 = client.get("/api/v1/weather?lat=22.5726&lon=88.3639")
    assert res1.status_code == 200
    res2 = client.get("/api/v1/weather?lat=22.5726&lon=88.3639")
    assert res2.status_code == 200
    # Cached response has identical observed_at timestamp
    assert res1.json()["observed_at"] == res2.json()["observed_at"]

def test_weather_impact_rules_deterministic():
    """Test deterministic agronomic rule mapping across various weather conditions."""
    # Test extreme heat
    adv_heat = weather_impact_service.evaluate_weather_impact(
        temperature=39.0,
        humidity=35,
        wind_speed=2.0,
        condition="Clear",
        rainfall=None
    )
    assert adv_heat.severity == "HIGH"
    assert "Heat Stress" in adv_heat.weather_hazard

    # Test prolonged wetness / high humidity
    adv_wet = weather_impact_service.evaluate_weather_impact(
        temperature=25.0,
        humidity=92,
        wind_speed=1.5,
        condition="Rain",
        rainfall=12.0
    )
    assert adv_wet.severity in ["MODERATE", "HIGH"]
    assert "Wetness" in adv_wet.weather_hazard or "Foliar" in adv_wet.weather_hazard

    # Test baseline favorable conditions
    adv_base = weather_impact_service.evaluate_weather_impact(
        temperature=22.0,
        humidity=55,
        wind_speed=2.5,
        condition="Clear",
        rainfall=None
    )
    assert adv_base.severity == "LOW"
    assert "Normal" in adv_base.weather_hazard or "Baseline" in adv_base.weather_hazard

def test_weather_independent_from_disease_prediction():
    """
    CRITICAL INVARIANT TEST:
    Weather layer must NEVER alter or couple to the ML inference model.
    A test leaf image prediction must yield identical confidence, top-1,
    top-3, and class predictions regardless of whether weather was called.
    """
    img = Image.new("RGB", (384, 384), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    # Predict before weather call
    pred_res1 = client.post(
        "/api/v1/predict",
        files={"image": ("leaf.jpg", image_bytes, "image/jpeg")},
        data={"include_gradcam": "false"}
    )
    assert pred_res1.status_code == 200
    data1 = pred_res1.json()

    # Call weather API
    weather_res = client.get("/api/v1/weather?lat=22.5726&lon=88.3639")
    assert weather_res.status_code == 200

    # Predict after weather call
    pred_res2 = client.post(
        "/api/v1/predict",
        files={"image": ("leaf.jpg", image_bytes, "image/jpeg")},
        data={"include_gradcam": "false"}
    )
    assert pred_res2.status_code == 200
    data2 = pred_res2.json()

    # Invariant: identical disease class and confidence
    assert data1["crop"] == data2["crop"]
    assert data1["disease"] == data2["disease"]
    assert data1["confidence"] == data2["confidence"]
    assert len(data1["top_predictions"]) == len(data2["top_predictions"])
    assert data1["top_predictions"][0]["raw_class"] == data2["top_predictions"][0]["raw_class"]
    assert data1["top_predictions"][0]["confidence"] == data2["top_predictions"][0]["confidence"]
