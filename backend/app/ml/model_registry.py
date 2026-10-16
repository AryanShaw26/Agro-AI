import time
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from PIL import Image
import torch

from app.core.config import settings
from app.ml.model_metadata import load_and_validate_metadata, ModelMetadata
from app.ml.preprocess import build_metadata_transforms, preprocess_image_tensor
from app.ml.model_loader import (
    build_efficientnet_v2_s_from_metadata,
    load_archived_efficientnet_b0,
    resolve_target_layer
)
from app.ml.class_map import CLASS_NAMES, parse_raw_class
from app.services.gradcam_service import GradCAMService

class ModelAdapter(ABC):
    @abstractmethod
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Runs inference and returns standard prediction dictionary."""
        pass

    @abstractmethod
    def explain(self, image: Image.Image, prediction_id: str, target_class_idx: int) -> Dict[str, Any]:
        """Generates Grad-CAM visual explanation."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def metadata_dict(self) -> Dict[str, Any]:
        pass


class EfficientNetV2SGradCAMAdapter(ModelAdapter):
    """
    Production Adapter for Model 2: EfficientNetV2-S with Integrated Grad-CAM.
    Driven strictly by efficientnetv2_s_metadata.json.
    """
    def __init__(self, metadata_path: str = None, checkpoint_path: str = None):
        meta_path = metadata_path or settings.MODEL_METADATA_PATH
        ckpt_path = checkpoint_path or settings.MODEL_PATH

        self.metadata: ModelMetadata = load_and_validate_metadata(meta_path)
        self._version = self.metadata.model_version
        self._model_name = self.metadata.display_name or self.metadata.model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Build metadata-driven transforms
        self.transforms = build_metadata_transforms(
            self.metadata.image_size,
            self.metadata.mean,
            self.metadata.std
        )

        # Build model and resolve Grad-CAM target layer
        self.model, self.device, self.target_layer = build_efficientnet_v2_s_from_metadata(
            self.metadata, ckpt_path, self.device
        )

        # Initialize integrated Grad-CAM service
        self.gradcam_service = GradCAMService(self.model, self.target_layer, self.device)

    @property
    def version(self) -> str:
        return self._version

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        return self.metadata.model_dump()

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        # Preprocess tensor strictly using metadata transforms
        tensor = preprocess_image_tensor(image, self.transforms).to(self.device)
        
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]
        
        top_k = 3
        top_probs, top_indices = torch.topk(probabilities, k=top_k)
        
        top_predictions: List[Dict[str, Any]] = []
        for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
            raw_class = self.metadata.class_names[idx] if idx < len(self.metadata.class_names) else CLASS_NAMES[idx]
            parsed = parse_raw_class(raw_class)
            top_predictions.append({
                "class_index": idx,
                "raw_class": raw_class,
                "crop": parsed["crop"],
                "disease": parsed["disease"],
                "is_healthy": parsed["is_healthy"],
                "confidence": round(float(prob), 4),
                "slug": parsed["slug"]
            })
            
        top_1 = top_predictions[0]
        processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        return {
            "crop": top_1["crop"],
            "disease": top_1["disease"],
            "is_healthy": top_1["is_healthy"],
            "confidence": top_1["confidence"],
            "raw_class": top_1["raw_class"],
            "slug": top_1["slug"],
            "top_predictions": top_predictions,
            "model_version": self.version,
            "model_name": self.model_name,
            "processing_time_ms": processing_time_ms,
            "preprocessed_tensor": tensor
        }

    def explain(self, image: Image.Image, prediction_id: str, target_class_idx: int) -> Dict[str, Any]:
        tensor = preprocess_image_tensor(image, self.transforms)
        return self.gradcam_service.process_and_cache(
            prediction_id, image, tensor, target_class_idx
        )


class EfficientNetB0Adapter(ModelAdapter):
    """
    Archived Adapter for EfficientNet-B0 (retained for rollback & historical scan support).
    """
    def __init__(self, checkpoint_path: str = None):
        self._version = "efficientnet-b0-v1"
        self._model_name = "EfficientNet-B0 PlantVillage Classifier (Archived Rollback)"
        ckpt_path = checkpoint_path or settings.FALLBACK_MODEL_PATH
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.device = load_archived_efficientnet_b0(ckpt_path, device=self.device)
        self.target_layer = self.model.conv_head if hasattr(self.model, "conv_head") else None
        self.gradcam_service = GradCAMService(self.model, self.target_layer, self.device) if self.target_layer else None

    @property
    def version(self) -> str:
        return self._version

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "model_version": self.version,
            "architecture": "efficientnet_b0",
            "num_classes": 38,
            "metrics": {"test_accuracy": 0.9943, "test_macro_f1": 0.9914}
        }

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        start_time = time.perf_counter()
        from app.ml.preprocess import default_transform
        tensor = preprocess_image_tensor(image, default_transform).to(self.device)
        
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]
        
        top_k = 3
        top_probs, top_indices = torch.topk(probabilities, k=top_k)
        
        top_predictions: List[Dict[str, Any]] = []
        for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
            raw_class = CLASS_NAMES[idx]
            parsed = parse_raw_class(raw_class)
            top_predictions.append({
                "class_index": idx,
                "raw_class": raw_class,
                "crop": parsed["crop"],
                "disease": parsed["disease"],
                "is_healthy": parsed["is_healthy"],
                "confidence": round(float(prob), 4),
                "slug": parsed["slug"]
            })
            
        top_1 = top_predictions[0]
        processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        return {
            "crop": top_1["crop"],
            "disease": top_1["disease"],
            "is_healthy": top_1["is_healthy"],
            "confidence": top_1["confidence"],
            "raw_class": top_1["raw_class"],
            "slug": top_1["slug"],
            "top_predictions": top_predictions,
            "model_version": self.version,
            "model_name": self.model_name,
            "processing_time_ms": processing_time_ms,
            "preprocessed_tensor": tensor
        }

    def explain(self, image: Image.Image, prediction_id: str, target_class_idx: int) -> Dict[str, Any]:
        if not self.gradcam_service:
            return {"available": False, "reason": "Target layer unavailable on archived model"}
        from app.ml.preprocess import default_transform
        tensor = preprocess_image_tensor(image, default_transform)
        return self.gradcam_service.process_and_cache(
            prediction_id, image, tensor, target_class_idx
        )


class ModelRegistry:
    _instance = None
    _adapter: ModelAdapter = None
    _fallback_adapter: ModelAdapter = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        """
        Initializes the active model adapter (EfficientNetV2-S).
        Safely rolls back to EfficientNet-B0 if V2-S initialization encounters missing files.
        """
        if self._adapter is None:
            try:
                print(f"[ModelRegistry] Attempting to load active model: EfficientNetV2-S with Grad-CAM...")
                self._adapter = EfficientNetV2SGradCAMAdapter()
                print(f"[ModelRegistry] Active model initialized: {self._adapter.model_name} (Version: {self._adapter.version})")
            except Exception as e:
                print(f"[ModelRegistry WARNING] Could not load EfficientNetV2-S: {e}")
                print(f"[ModelRegistry] Rolling back to archived EfficientNet-B0 model...")
                try:
                    self._adapter = EfficientNetB0Adapter()
                    print(f"[ModelRegistry] Rollback successful: Active model is {self._adapter.model_name}")
                except Exception as rollback_err:
                    print(f"[ModelRegistry CRITICAL] Rollback also failed: {rollback_err}")
                    raise rollback_err

    def get_active_model(self) -> ModelAdapter:
        if self._adapter is None:
            self.initialize()
        return self._adapter

    def switch_to_rollback_b0(self):
        """Manual rollback trigger."""
        self._adapter = EfficientNetB0Adapter()
        return self._adapter

model_registry = ModelRegistry.get_instance()
