import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ModelMetadata(BaseModel):
    model_name: str
    model_version: str
    architecture: str
    variant: Optional[str] = "s"
    framework: Optional[str] = "torchvision"
    num_classes: int = 38
    image_size: List[int] = Field(default_factory=lambda: [384, 384])
    mean: List[float] = Field(default_factory=lambda: [0.485, 0.456, 0.406])
    std: List[float] = Field(default_factory=lambda: [0.229, 0.224, 0.225])
    gradcam_layer: str = "features.7"
    checkpoint_file: Optional[str] = "efficientnetv2_s_38class_gradcam_best.pth"
    class_names: List[str]
    metrics: Dict[str, Any] = Field(default_factory=dict)
    explainability: Dict[str, Any] = Field(default_factory=dict)

def load_and_validate_metadata(metadata_path: str) -> ModelMetadata:
    """
    Loads and strictly validates model deployment contract metadata JSON.
    Raises FileNotFoundError or ValueError if invalid.
    """
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Model metadata file not found at: {metadata_path}")
        
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse model metadata JSON: {e}")

    # Validate essential fields
    required_fields = ["architecture", "num_classes", "class_names", "image_size", "mean", "std"]
    missing = [rf for rf in required_fields if rf not in data]
    if missing:
        raise ValueError(f"Invalid model metadata contract. Missing required fields: {missing}")

    if data.get("num_classes") != 38:
        raise ValueError(f"Expected 38 classes, found {data.get('num_classes')}")

    if len(data.get("class_names", [])) != 38:
        raise ValueError(f"class_names length must be exactly 38, found {len(data.get('class_names', []))}")

    return ModelMetadata(**data)
