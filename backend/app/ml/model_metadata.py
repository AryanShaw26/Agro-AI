import os
import json
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

class ModelMetadata(BaseModel):
    model_name: str = "EfficientNetV2-S Plant Disease Classifier with Integrated Grad-CAM"
    display_name: Optional[str] = None
    model_version: str = "efficientnetv2-s-gradcam-v1"
    architecture: str = "tf_efficientnetv2_s.in1k"
    variant: Optional[str] = "s"
    framework: Optional[str] = "timm"
    num_classes: int = 38
    image_size: List[int] = Field(default_factory=lambda: [260, 260])
    mean: List[float] = Field(default_factory=lambda: [0.485, 0.456, 0.406])
    std: List[float] = Field(default_factory=lambda: [0.229, 0.224, 0.225])
    gradcam_layer: str = "conv_head"
    checkpoint_file: Optional[str] = "efficientnetv2_s_38class_gradcam_best.pth"
    class_names: List[str]
    metrics: Dict[str, Any] = Field(default_factory=dict)
    explainability: Dict[str, Any] = Field(default_factory=dict)

def load_and_validate_metadata(metadata_path: str) -> ModelMetadata:
    """
    Loads and normalizes model deployment contract metadata JSON.
    Supports both canonical AgroAI metadata and user training export schemas.
    """
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Model metadata file not found at: {metadata_path}")
        
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse model metadata JSON: {e}")

    # Normalize image_size (int -> [int, int])
    raw_size = data.get("image_size", 260)
    if isinstance(raw_size, int):
        data["image_size"] = [raw_size, raw_size]
    elif isinstance(raw_size, (list, tuple)) and len(raw_size) == 1:
        data["image_size"] = [raw_size[0], raw_size[0]]

    # Normalize gradcam_target -> gradcam_layer
    if "gradcam_target" in data and "gradcam_layer" not in data:
        data["gradcam_layer"] = data["gradcam_target"]

    # Normalize architecture / model_name
    if "architecture" not in data:
        data["architecture"] = data.get("model_name", "tf_efficientnetv2_s.in1k")

    # Normalize framework
    if "framework" not in data:
        arch = data.get("architecture", "")
        if "tf_" in arch or "in1k" in arch or "timm" in arch:
            data["framework"] = "timm"
        else:
            data["framework"] = "torchvision"

    # Default normalization if omitted
    if "mean" not in data:
        data["mean"] = [0.485, 0.456, 0.406]
    if "std" not in data:
        data["std"] = [0.229, 0.224, 0.225]

    # Collect performance metrics if flattened in raw json
    metrics = data.get("metrics", {})
    for metric_key in ["best_validation_f1", "test_accuracy_tta", "test_macro_f1_tta", "val_f1", "val_accuracy"]:
        if metric_key in data and metric_key not in metrics:
            metrics[metric_key] = data[metric_key]
    data["metrics"] = metrics

    # Normalize checkpoint file
    if "checkpoint" in data and "checkpoint_file" not in data:
        data["checkpoint_file"] = os.path.basename(data["checkpoint"])

    # Validate essential fields
    if "class_names" not in data or len(data["class_names"]) != 38:
        raise ValueError(f"class_names must be present and contain exactly 38 classes, found {len(data.get('class_names', []))}")

    data["num_classes"] = len(data["class_names"])

    return ModelMetadata(**data)
