import io
from PIL import Image
import torch
import torchvision.transforms as transforms

# Standard ImageNet normalization matching training
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])

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

def preprocess_image_tensor(image: Image.Image) -> torch.Tensor:
    """
    Prepares tensor shape [1, 3, 224, 224] with ImageNet normalization.
    """
    tensor = inference_transform(image)
    return tensor.unsqueeze(0)

