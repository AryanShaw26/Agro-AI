from fastapi import APIRouter
from app.api.v1.predict import router as predict_router
from app.api.v1.diseases import router as diseases_router
from app.api.v1.history import router as history_router
from app.api.v1.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(predict_router, tags=["Prediction"])
api_router.include_router(diseases_router, tags=["Diseases & Knowledge Base"])
api_router.include_router(history_router, tags=["Scan History"])
api_router.include_router(reports_router, tags=["Reports"])
