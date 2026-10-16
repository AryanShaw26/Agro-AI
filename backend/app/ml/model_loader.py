import os
import torch
import torchvision.models as models
import timm
from app.ml.model_metadata import ModelMetadata

def extract_state_dict(checkpoint):
    """
    Safely unboxes state_dict from various checkpoint packaging structures.
    """
    if isinstance(checkpoint, dict):
        if "model_state_dict" in checkpoint:
            return checkpoint["model_state_dict"]
        elif "state_dict" in checkpoint:
            return checkpoint["state_dict"]
        elif "model" in checkpoint:
            return checkpoint["model"]
    return checkpoint

def resolve_target_layer(model: torch.nn.Module, layer_name: str) -> torch.nn.Module:
    """
    Recursively resolves target layer from dot-notation string, e.g. 'features.7' or 'conv_head'.
    Gracefully falls back to architecture-appropriate feature layer if layer_name differs.
    """
    try:
        curr = model
        for part in layer_name.split("."):
            if part.isdigit():
                curr = curr[int(part)]
            elif hasattr(curr, part):
                curr = getattr(curr, part)
            else:
                raise AttributeError(f"Layer '{part}' not found")
        return curr
    except Exception:
        # Fallback for timm models
        if hasattr(model, "conv_head"):
            return model.conv_head
        # Fallback for torchvision models
        if hasattr(model, "features"):
            return model.features[-1]
        raise AttributeError(f"Could not resolve Grad-CAM layer '{layer_name}' in module '{type(model).__name__}'")

def build_efficientnet_v2_s_from_metadata(
    metadata: ModelMetadata,
    checkpoint_path: str,
    device: torch.device = None
):
    """
    Instantiates EfficientNetV2-S, loads weights from checkpoint, and validates output.
    Automatically detects and handles both timm and torchvision checkpoint formats.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"V2-S Checkpoint not found at: {checkpoint_path}")

    raw_ckpt = torch.load(checkpoint_path, map_location=device)
    state_dict = extract_state_dict(raw_ckpt)
    state_keys = list(state_dict.keys())

    # Detect whether checkpoint is timm or torchvision
    is_timm = any(k.startswith("conv_stem") or k.startswith("blocks.") or "conv_head" in k for k in state_keys)

    if is_timm or metadata.framework == "timm" or "tf_efficientnetv2" in metadata.architecture:
        arch = metadata.architecture if ("efficientnet" in metadata.architecture and "in1k" in metadata.architecture) else "tf_efficientnetv2_s.in1k"
        model = timm.create_model(arch, num_classes=metadata.num_classes, pretrained=False)
    else:
        model = models.efficientnet_v2_s(weights=None, num_classes=metadata.num_classes)

    msg = model.load_state_dict(state_dict, strict=False)
    print(f"[ModelLoader] Loaded EfficientNetV2-S weights: {msg}")

    model.to(device)
    model.eval()

    # Startup validation: verify 38 classes output and target Grad-CAM layer
    h, w = metadata.image_size[0], metadata.image_size[1]
    test_input = torch.randn(1, 3, h, w).to(device)
    with torch.no_grad():
        out = model(test_input)
    if out.shape[-1] != metadata.num_classes:
        raise ValueError(f"Model output mismatch: expected {metadata.num_classes}, got {out.shape[-1]}")

    target_layer = resolve_target_layer(model, metadata.gradcam_layer)
    if target_layer is None:
        raise ValueError(f"Could not resolve Grad-CAM layer: {metadata.gradcam_layer}")

    print(f"[ModelLoader] EfficientNetV2-S verified successfully. Target Grad-CAM layer: {metadata.gradcam_layer}")
    return model, device, target_layer

def load_archived_efficientnet_b0(checkpoint_path: str, num_classes: int = 38, device: torch.device = None):
    """
    Loads archived EfficientNet-B0 model for rollback / fallback purposes.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Archived B0 checkpoint not found at {checkpoint_path}")

    model = timm.create_model("efficientnet_b0", num_classes=num_classes, pretrained=False)
    ckpt = torch.load(checkpoint_path, map_location=device)
    state_dict = extract_state_dict(ckpt)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model, device
