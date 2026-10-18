import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

# Determine canonical project base paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))               # backend/app/core
APP_DIR = os.path.dirname(CURRENT_DIR)                                 # backend/app
BACKEND_DIR = os.path.dirname(APP_DIR)                                # backend
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)                            # AgroAI root

def resolve_model_file(filename: Optional[str]) -> str:
    """
    Intelligently resolves model or metadata file across common placement directories:
    1. Absolute path if existing
    2. Relative to current working directory
    3. Relative to PROJECT_ROOT (c:\\...\\AgroAI)
    4. Relative to BACKEND_DIR (c:\\...\\AgroAI\\backend)
    5. Stripping leading 'backend/' when running inside backend/
    6. backend/app/models/<basename>
    7. Models/<basename>
    """
    if not filename:
        return ""
        
    normalized = filename.replace("\\", "/")
    
    # 1. Absolute path
    if os.path.isabs(filename) and os.path.exists(filename):
        return os.path.abspath(filename)
        
    # 2. Direct relative to cwd
    if os.path.exists(filename):
        return os.path.abspath(filename)
        
    # 3. Relative to project root
    p_root = os.path.join(PROJECT_ROOT, normalized)
    if os.path.exists(p_root):
        return os.path.abspath(p_root)
        
    # 4. Relative to backend directory
    p_backend = os.path.join(BACKEND_DIR, normalized)
    if os.path.exists(p_backend):
        return os.path.abspath(p_backend)
        
    # 5. Stripped leading 'backend/' if running inside backend/
    if normalized.startswith("backend/"):
        stripped = normalized[len("backend/"):]
        p_strip = os.path.join(BACKEND_DIR, stripped)
        if os.path.exists(p_strip):
            return os.path.abspath(p_strip)
            
    # 6. Look inside backend/app/models by basename
    base_name = os.path.basename(normalized)
    p_app_models = os.path.join(APP_DIR, "models", base_name)
    if os.path.exists(p_app_models):
        return os.path.abspath(p_app_models)
        
    # 7. Look inside root Models by basename
    p_root_models = os.path.join(PROJECT_ROOT, "Models", base_name)
    if os.path.exists(p_root_models):
        return os.path.abspath(p_root_models)
        
    # Return best resolved path candidate
    return os.path.abspath(os.path.join(APP_DIR, "models", base_name))

# Canonical default SQLite database location at project root
DEFAULT_DB_FILE = os.path.join(PROJECT_ROOT, "agroai.db")
DEFAULT_DB_URL = f"sqlite:///{DEFAULT_DB_FILE.replace(os.sep, '/')}"

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroAI Plant Disease Detection Platform"
    API_V1_STR: str = "/api/v1"
    
    # Model Configuration (EfficientNetV2-S + Metadata Contract)
    MODEL_METADATA_PATH: str = "backend/app/models/efficientnetv2_s_metadata.json"
    MODEL_PATH: str = "backend/app/models/efficientnetv2_s_38class_gradcam_best.pth"
    FALLBACK_MODEL_PATH: Optional[str] = None
    MODEL_VERSION: str = "efficientnetv2-s-gradcam-v1"
    CONFIDENCE_THRESHOLD: float = 0.70
    
    # Database
    DATABASE_URL: str = DEFAULT_DB_URL
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Upload limits
    MAX_IMAGE_SIZE_BYTES: int = 15 * 1024 * 1024  # 15MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]
    
    # OpenWeather API Configuration (Backend-only, never expose to client)
    OPENWEATHER_API_KEY: Optional[str] = None
    WEATHER_CACHE_TTL_SECONDS: int = 600  # 10 minutes cache TTL per OpenWeather update guidelines

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env", os.path.join(PROJECT_ROOT, ".env"), os.path.join(BACKEND_DIR, ".env")),
        extra="ignore"
    )

    @model_validator(mode="after")
    def resolve_all_paths(self):
        self.MODEL_METADATA_PATH = resolve_model_file(self.MODEL_METADATA_PATH)
        self.MODEL_PATH = resolve_model_file(self.MODEL_PATH)
        if self.FALLBACK_MODEL_PATH:
            resolved_fallback = resolve_model_file(self.FALLBACK_MODEL_PATH)
            self.FALLBACK_MODEL_PATH = resolved_fallback if os.path.exists(resolved_fallback) else None
        if self.DATABASE_URL.startswith("sqlite:///./"):
            rel_part = self.DATABASE_URL.replace("sqlite:///./", "")
            abs_db = os.path.join(PROJECT_ROOT, rel_part).replace(os.sep, "/")
            self.DATABASE_URL = f"sqlite:///{abs_db}"
        return self

settings = Settings()
