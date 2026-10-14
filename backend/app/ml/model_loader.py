import os
import torch
import timm
from app.core.config import settings

def load_efficientnet_b0(checkpoint_path: str = None, num_classes: int = 38, device: torch.device = None):
    """
    Builds EfficientNet-B0 architecture and loads trained checkpoint weights.
    """
    if checkpoint_path is None:
        checkpoint_path = settings.MODEL_PATH
        
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Model checkpoint not found at {checkpoint_path}")

    # Build EfficientNet-B0 classifier matching training
    model = timm.create_model("efficientnet_b0", num_classes=num_classes, pretrained=False)
    
    # Load state dict
    checkpoint = torch.load(checkpoint_path, map_location=device)
    state_dict = checkpoint["model_state_dict"] if "model_state_dict" in checkpoint else checkpoint
    
    msg = model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model, device
