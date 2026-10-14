import io
import json
import uuid
import base64
from PIL import Image
from sqlalchemy.orm import Session

from app.core.config import settings
from app.ml.preprocess import validate_and_load_image
from app.ml.model_registry import model_registry
from app.services.knowledge_service import knowledge_service
from app.services.gradcam_service import generate_gradcam_overlay
from app.models.db_models import ScanPrediction
from app.schemas.predict import PredictionResponse, TopPredictionItem

class InferenceService:
    @staticmethod
    def process_and_predict(
        image_bytes: bytes,
        db: Session,
        include_gradcam: bool = True
    ) -> PredictionResponse:
        # 1. Validate & load image
        image = validate_and_load_image(image_bytes)

        # 2. Run inference via active model adapter
        adapter = model_registry.get_active_model()
        pred_dict = adapter.predict(image)

        # 3. Confidence policy
        confidence = pred_dict["confidence"]
        threshold = settings.CONFIDENCE_THRESHOLD
        confidence_state = "confident" if confidence >= threshold else "uncertain"

        # 4. Knowledge Base lookup (No GenAI)
        knowledge = knowledge_service.get_by_raw_class(db, pred_dict["raw_class"])

        # 5. Optional Grad-CAM
        gradcam_image = None
        if include_gradcam:
            try:
                top_class_idx = pred_dict["top_predictions"][0]["class_index"]
                gradcam_image = generate_gradcam_overlay(image, target_class_idx=top_class_idx)
            except Exception as e:
                print(f"[Grad-CAM Warning] Could not generate Grad-CAM: {e}")
                gradcam_image = None

        # 6. Generate thumbnail for persistence (max 256x256 JPEG)
        thumb = image.copy()
        thumb.thumbnail((256, 256))
        buf = io.BytesIO()
        thumb.save(buf, format="JPEG", quality=75)
        thumb_uri = f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"

        # 7. Persist to database
        prediction_id = str(uuid.uuid4())
        scan_record = ScanPrediction(
            id=prediction_id,
            crop=pred_dict["crop"],
            disease=pred_dict["disease"],
            raw_class=pred_dict["raw_class"],
            confidence=confidence,
            confidence_state=confidence_state,
            top_predictions_json=json.dumps(pred_dict["top_predictions"]),
            image_data_uri=thumb_uri,
            model_version=pred_dict["model_version"],
            processing_time_ms=pred_dict["processing_time_ms"]
        )
        try:
            db.add(scan_record)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[DB Warning] Could not persist scan record: {e}")

        top_pred_items = [
            TopPredictionItem(
                crop=p["crop"],
                disease=p["disease"],
                confidence=p["confidence"],
                is_healthy=p["is_healthy"],
                slug=p["slug"],
                raw_class=p.get("raw_class")
            )
            for p in pred_dict["top_predictions"]
        ]

        return PredictionResponse(
            prediction_id=prediction_id,
            crop=pred_dict["crop"],
            disease=pred_dict["disease"],
            confidence=confidence,
            confidence_state=confidence_state,
            is_healthy=pred_dict["is_healthy"],
            raw_class=pred_dict["raw_class"],
            slug=pred_dict["slug"],
            model_version=pred_dict["model_version"],
            processing_time_ms=pred_dict["processing_time_ms"],
            top_predictions=top_pred_items,
            knowledge=knowledge,
            gradcam_image=gradcam_image,
            image_preview_url=thumb_uri
        )

inference_service = InferenceService()

