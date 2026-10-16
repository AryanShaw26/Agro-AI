import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine canonical project base paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))               # backend/app/core
APP_DIR = os.path.dirname(CURRENT_DIR)                                 # backend/app
BACKEND_DIR = os.path.dirname(APP_DIR)                                # backend
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)                            # AgroAI root

def resolve_model_file(filename: str, preferred_subdirs: List[str] = None) -> str:
    """
    Intelligently resolves model or metadata file across common user placement directories:
    1. backend/app/models/
    2. Models/ (repo root)
    3. backend/models/
    4. Exact or relative path provided
    """
    if os.path.isabs(filename) and os.path.exists(filename):
        return filename
    if os.path.exists(filename):
        return os.path.abspath(filename)
        
    base_name = os.path.basename(filename)
    candidates = [
        os.path.join(APP_DIR, "models", base_name),
        os.path.join(PROJECT_ROOT, "Models", base_name),
        os.path.join(BACKEND_DIR, "models", base_name),
        os.path.join(PROJECT_ROOT, filename),
        os.path.join(BACKEND_DIR, filename),
        os.path.join(APP_DIR, filename),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    
    # Return best absolute candidate if none found yet
    return os.path.abspath(candidates[0])

# Auto-resolve canonical default paths
DEFAULT_METADATA_PATH = resolve_model_file("efficientnetv2_s_metadata.json")
DEFAULT_MODEL_PATH = resolve_model_file("efficientnetv2_s_38class_gradcam_best.pth")
DEFAULT_FALLBACK_PATH = resolve_model_file("efficientnet_b0_best.pth")

# Canonical default SQLite database location at project root
DEFAULT_DB_FILE = os.path.join(PROJECT_ROOT, "agroai.db")
DEFAULT_DB_URL = f"sqlite:///{DEFAULT_DB_FILE.replace(os.sep, '/')}"

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroAI Plant Disease Detection Platform"
    API_V1_STR: str = "/api/v1"
    
    # Model Configuration (EfficientNetV2-S + Metadata Contract)
    MODEL_METADATA_PATH: str = os.getenv("MODEL_METADATA_PATH", DEFAULT_METADATA_PATH)
    MODEL_PATH: str = os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)
    FALLBACK_MODEL_PATH: str = os.getenv("FALLBACK_MODEL_PATH", DEFAULT_FALLBACK_PATH)
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "efficientnetv2-s-gradcam-v1")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Upload limits
    MAX_IMAGE_SIZE_BYTES: int = 15 * 1024 * 1024  # 15MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".webp"}

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
