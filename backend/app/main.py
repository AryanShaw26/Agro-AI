import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import api_router
from app.db.seed_data import seed_database
from app.ml.model_registry import model_registry

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[AgroAI] Initializing platform...")
    # Seed knowledge base if not already seeded
    seed_database()
    # Pre-warm model in registry
    print("[AgroAI] Pre-loading EfficientNet-B0 model weights...")
    model_registry.initialize()
    print("[AgroAI] Startup sequence complete.")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AgroAI Plant Disease Detection Platform — Model 1 EfficientNet-B0 + Verified Agricultural Knowledge Base (No GenAI)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AgroAI Inference & Knowledge API",
        "model_version": settings.MODEL_VERSION,
        "classes_supported": 38,
        "genai_enabled": False
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to AgroAI Plant Disease Detection API",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
        "model": "Model 1: EfficientNet-B0",
        "philosophy": "Scan. Understand. Protect. (No GenAI)"
    }
