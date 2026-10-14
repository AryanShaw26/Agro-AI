import io
import base64
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F

from app.ml.preprocess import preprocess_image_tensor
from app.ml.model_registry import model_registry

def generate_gradcam_overlay(image: Image.Image, target_class_idx: int = None) -> str:
    """
    Computes Grad-CAM heatmap on the last convolutional layer of EfficientNet-B0 (conv_head),
    blends it with the original image, and returns a base64 data URI string.
    """
    adapter = model_registry.get_active_model()
    model = adapter.model
    device = adapter.device
    
    # Save original size
    orig_w, orig_h = image.size
    
    # Preprocess tensor
    input_tensor = preprocess_image_tensor(image).to(device)
    input_tensor.requires_grad = True

    # Target the last conv layer in timm's EfficientNet-B0: model.conv_head
    target_layer = model.conv_head

    activations = []
    gradients = []

    def forward_hook(module, input, output):
        activations.append(output)

    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    h1 = target_layer.register_forward_hook(forward_hook)
    h2 = target_layer.register_full_backward_hook(backward_hook)

    try:
        model.zero_grad()
        output = model(input_tensor)
        
        if target_class_idx is None:
            target_class_idx = output.argmax(dim=1).item()

        score = output[0, target_class_idx]
        score.backward()

        # Extract captured activations and gradients
        act = activations[0].detach()  # [1, C, H, W]
        grad = gradients[0].detach()   # [1, C, H, W]

        # Global average pooling on gradients -> channel weights
        weights = torch.mean(grad, dim=(2, 3), keepdim=True)  # [1, C, 1, 1]

        # Weighted combination of activation maps
        cam = torch.sum(weights * act, dim=1, keepdim=True)    # [1, 1, H, W]
        cam = F.relu(cam)  # Only positive influence

        cam = cam.squeeze().cpu().numpy()
        if cam.max() > 0:
            cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        else:
            cam = np.zeros_like(cam)

        # Resize CAM to match original image dimensions using PIL
        cam_img = Image.fromarray(np.uint8(255 * cam)).resize((orig_w, orig_h), resample=Image.BILINEAR)
        cam_array = np.array(cam_img) / 255.0

        # Create JET colormap approximation for heatmap
        # Jet: blue (0) -> cyan (0.25) -> green (0.5) -> yellow (0.75) -> red (1)
        r = np.clip(1.5 - np.abs(4 * cam_array - 3), 0, 1)
        g = np.clip(1.5 - np.abs(4 * cam_array - 2), 0, 1)
        b = np.clip(1.5 - np.abs(4 * cam_array - 1), 0, 1)
        heatmap = np.stack([r, g, b], axis=-1) * 255.0

        # Alpha blend with original image (45% heatmap, 55% original)
        orig_np = np.array(image.convert("RGB")).astype(np.float32)
        blended = (0.45 * heatmap + 0.55 * orig_np).clip(0, 255).astype(np.uint8)

        # Encode to base64
        overlay_pil = Image.fromarray(blended)
        buf = io.BytesIO()
        overlay_pil.save(buf, format="JPEG", quality=85)
        base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{base64_str}"

    finally:
        h1.remove()
        h2.remove()

