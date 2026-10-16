import io
from typing import List, Tuple
from PIL import Image
import torch
import torchvision.transforms as transforms

def build_metadata_transforms(
    image_size: List[int],
    mean: List[float],
    std: List[float]
) -> transforms.Compose:
    """
    Constructs torchvision preprocessing pipeline dynamically driven by metadata contract.
    """
    if isinstance(image_size, int):
        size_tuple = (image_size, image_size)
    elif len(image_size) == 2:
        size_tuple = (image_size[0], image_size[1])
    else:
        size_tuple = (image_size[0], image_size[0])
    return transforms.Compose([
        transforms.Resize(size_tuple),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

# Default fallback transforms (ImageNet standard)
default_transform = build_metadata_transforms([384, 384], [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

def validate_and_load_image(image_bytes: bytes) -> Image.Image:
    """
    Validates image bytes, verifies integrity, and converts to RGB PIL Image.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # Check for corruption
        
        # Re-open after verify() because verify() invalidates the file pointer
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        return image
    except Exception as e:
        raise ValueError(f"Invalid or corrupted image format: {str(e)}")

def preprocess_image_tensor(image: Image.Image, transform: transforms.Compose = None) -> torch.Tensor:
    """
    Prepares tensor [1, 3, H, W] with metadata-driven normalization.
    """
    tf = transform or default_transform
    tensor = tf(image)
    return tensor.unsqueeze(0)
