import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroAI Plant Disease Detection Platform"
    API_V1_STR: str = "/api/v1"
    
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "Models/efficientnet_b0_best.pth")
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "efficientnet-b0-v1")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agroai.db")
    
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
