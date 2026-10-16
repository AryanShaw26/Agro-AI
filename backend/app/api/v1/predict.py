import io
import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status, Response
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.predict import PredictionResponse, TopPredictionItem, GradCAMMetadata
from app.services.inference_service import inference_service
from app.models.db_models import ScanPrediction
from app.services.knowledge_service import knowledge_service
from app.ml.model_registry import model_registry

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict_plant_disease(
    image: UploadFile = File(..., description="Plant leaf image (JPG, PNG, WEBP)"),
    include_gradcam: bool = Form(default=True, description="Whether to include Grad-CAM heatmap"),
    db: Session = Depends(get_db)
):
    """
    Classifies uploaded plant leaf image into one of 38 classes using active model (EfficientNetV2-S),
    generates first-class Grad-CAM attention visualizations, and retrieves verified knowledge.
    """
    # 1. Validate file extension
    filename = image.filename or "unknown.jpg"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # 2. Read file content & validate size
    contents = await image.read()
    if len(contents) > settings.MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds the maximum limit of {settings.MAX_IMAGE_SIZE_BYTES // (1024*1024)}MB."
        )

    if len(contents) < 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is too small or empty."
        )

    # 3. Perform inference & knowledge lookup
    try:
        response = inference_service.process_and_predict(
            image_bytes=contents,
            db=db,
            include_gradcam=include_gradcam
        )
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {str(e)}")


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
def get_prediction_by_id(prediction_id: str, db: Session = Depends(get_db)):
    """
    Retrieves a past prediction record by its ID with full verified knowledge base details.
    """
    scan = db.query(ScanPrediction).filter_by(id=prediction_id).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction record not found")

    knowledge = knowledge_service.get_by_raw_class(db, scan.raw_class)
    top_preds = json.loads(scan.top_predictions_json)

    top_pred_items = [
        TopPredictionItem(
            crop=p["crop"],
            disease=p["disease"],
            confidence=p["confidence"],
            is_healthy=p["is_healthy"],
            slug=p["slug"],
            raw_class=p.get("raw_class")
        )
        for p in top_preds
    ]

    return PredictionResponse(
        prediction_id=scan.id,
        crop=scan.crop,
        disease=scan.disease,
        confidence=scan.confidence,
        confidence_state=scan.confidence_state,
        is_healthy="healthy" in scan.disease.lower(),
        raw_class=scan.raw_class,
        slug=top_pred_items[0].slug if top_pred_items else "result",
        model_version=scan.model_version,
        processing_time_ms=scan.processing_time_ms,
        top_predictions=top_pred_items,
        knowledge=knowledge,
        image_preview_url=scan.image_data_uri,
        gradcam=GradCAMMetadata(
            available=True,
            target_class=scan.raw_class,
            overlay_url=f"/api/v1/predictions/{scan.id}/gradcam",
            heatmap_url=f"/api/v1/predictions/{scan.id}/gradcam/heatmap"
        )
    )


@router.get("/predictions/{prediction_id}/gradcam")
def get_prediction_gradcam_overlay(prediction_id: str):
    """
    Returns the Grad-CAM blended overlay artifact as an image/jpeg stream.
    """
    adapter = model_registry.get_active_model()
    if hasattr(adapter, "gradcam_service") and adapter.gradcam_service:
        img_bytes = adapter.gradcam_service.get_artifact(prediction_id, "overlay")
        if img_bytes:
            return Response(content=img_bytes, media_type="image/jpeg")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grad-CAM overlay artifact expired or not found")


@router.get("/predictions/{prediction_id}/gradcam/heatmap")
def get_prediction_gradcam_heatmap(prediction_id: str):
    """
    Returns the raw Grad-CAM Jet heatmap artifact as an image/jpeg stream.
    """
    adapter = model_registry.get_active_model()
    if hasattr(adapter, "gradcam_service") and adapter.gradcam_service:
        img_bytes = adapter.gradcam_service.get_artifact(prediction_id, "heatmap")
        if img_bytes:
            return Response(content=img_bytes, media_type="image/jpeg")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grad-CAM heatmap artifact expired or not found")
