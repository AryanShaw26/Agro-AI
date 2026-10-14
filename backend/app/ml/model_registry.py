import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from PIL import Image
import torch

from app.core.config import settings
from app.ml.model_loader import load_efficientnet_b0
from app.ml.preprocess import preprocess_image_tensor
from app.ml.class_map import CLASS_NAMES, parse_raw_class

class ModelAdapter(ABC):
    @abstractmethod
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Runs inference and returns standard prediction dictionary."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass


class EfficientNetB0Adapter(ModelAdapter):
    def __init__(self, checkpoint_path: str = None):
        self._version = settings.MODEL_VERSION
        self.model, self.device = load_efficientnet_b0(checkpoint_path)

    @property
    def version(self) -> str:
        return self._version

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        # Preprocess to tensor [1, 3, 224, 224]
        tensor = preprocess_image_tensor(image).to(self.device)
        
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]
        
        # Top-3 predictions
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
            "processing_time_ms": processing_time_ms
        }


class ModelRegistry:
    _instance = None
    _adapter: ModelAdapter = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        if self._adapter is None:
            self._adapter = EfficientNetB0Adapter()

    def get_active_model(self) -> ModelAdapter:
        if self._adapter is None:
            self.initialize()
        return self._adapter

model_registry = ModelRegistry.get_instance()
