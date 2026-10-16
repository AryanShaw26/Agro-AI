import io
import base64
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F

class GradCAMService:
    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module, device: torch.device):
        self.model = model
        self.target_layer = target_layer
        self.device = device
        # Cache for streaming endpoints: {prediction_id: {"overlay": bytes, "heatmap": bytes}}
        self._artifact_cache: Dict[str, Dict[str, bytes]] = {}

    def generate_heatmap_and_overlay(
        self,
        image: Image.Image,
        input_tensor: torch.Tensor,
        target_class_idx: int,
        alpha: float = 0.45
    ) -> Tuple[np.ndarray, Image.Image, Image.Image]:
        """
        Executes Grad-CAM on target_layer and returns (raw_cam_array, heatmap_pil, overlay_pil).
        """
        orig_w, orig_h = image.size
        tensor = input_tensor.clone().detach().to(self.device)
        tensor.requires_grad = True

        activations = []
        gradients = []

        def forward_hook(module, input, output):
            activations.append(output)

        def backward_hook(module, grad_input, grad_output):
            gradients.append(grad_output[0])

        h1 = self.target_layer.register_forward_hook(forward_hook)
        h2 = self.target_layer.register_full_backward_hook(backward_hook)

        try:
            self.model.zero_grad()
            output = self.model(tensor)
            
            score = output[0, target_class_idx]
            score.backward()

            act = activations[0].detach()  # [1, C, H, W]
            grad = gradients[0].detach()   # [1, C, H, W]

            # Global average pooling on gradients -> channel weights
            weights = torch.mean(grad, dim=(2, 3), keepdim=True)
            cam = torch.sum(weights * act, dim=1, keepdim=True)
            cam = F.relu(cam)

            cam = cam.squeeze().cpu().numpy()
            if cam.max() > 0:
                cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
            else:
                cam = np.zeros_like(cam)

            # Resize CAM to match original image dimensions using PIL bilinear
            cam_pil = Image.fromarray(np.uint8(255 * cam)).resize((orig_w, orig_h), resample=Image.BILINEAR)
            cam_array = np.array(cam_pil) / 255.0

            # Jet colormap approximation: blue (0) -> cyan (0.25) -> green (0.5) -> yellow (0.75) -> red (1)
            r = np.clip(1.5 - np.abs(4 * cam_array - 3), 0, 1)
            g = np.clip(1.5 - np.abs(4 * cam_array - 2), 0, 1)
            b = np.clip(1.5 - np.abs(4 * cam_array - 1), 0, 1)
            heatmap_rgb = (np.stack([r, g, b], axis=-1) * 255.0).astype(np.uint8)
            heatmap_img = Image.fromarray(heatmap_rgb)

            # Blend with original leaf image
            orig_rgb = np.array(image.convert("RGB")).astype(np.float32)
            blended = (alpha * heatmap_rgb + (1 - alpha) * orig_rgb).clip(0, 255).astype(np.uint8)
            overlay_img = Image.fromarray(blended)

            return cam_array, heatmap_img, overlay_img

        finally:
            h1.remove()
            h2.remove()

    def process_and_cache(
        self,
        prediction_id: str,
        image: Image.Image,
        input_tensor: torch.Tensor,
        target_class_idx: int
    ) -> Dict[str, Any]:
        """
        Runs Grad-CAM, caches JPEG bytes for API endpoints, and returns URIs + base64 data.
        """
        _, heatmap_img, overlay_img = self.generate_heatmap_and_overlay(
            image, input_tensor, target_class_idx
        )

        # Buffer for overlay
        overlay_buf = io.BytesIO()
        overlay_img.save(overlay_buf, format="JPEG", quality=85)
        overlay_bytes = overlay_buf.getvalue()

        # Buffer for heatmap
        heatmap_buf = io.BytesIO()
        heatmap_img.save(heatmap_buf, format="JPEG", quality=85)
        heatmap_bytes = heatmap_buf.getvalue()

        # Cache in memory for endpoint downloads
        self._artifact_cache[prediction_id] = {
            "overlay": overlay_bytes,
            "heatmap": heatmap_bytes
        }

        # Base64 URIs for immediate UI rendering
        overlay_b64 = f"data:image/jpeg;base64,{base64.b64encode(overlay_bytes).decode('utf-8')}"
        heatmap_b64 = f"data:image/jpeg;base64,{base64.b64encode(heatmap_bytes).decode('utf-8')}"

        return {
            "available": True,
            "target_class_index": target_class_idx,
            "overlay_url": f"/api/v1/predictions/{prediction_id}/gradcam",
            "heatmap_url": f"/api/v1/predictions/{prediction_id}/gradcam/heatmap",
            "overlay_base64": overlay_b64,
            "heatmap_base64": heatmap_b64
        }

    def get_artifact(self, prediction_id: str, artifact_type: str = "overlay") -> Optional[bytes]:
        """
        Retrieves cached Grad-CAM image bytes for streaming endpoints.
        """
        entry = self._artifact_cache.get(prediction_id)
        if entry and artifact_type in entry:
            return entry[artifact_type]
        return None
