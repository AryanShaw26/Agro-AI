from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.predict import TopPredictionItem

class ScanHistoryItem(BaseModel):
    id: str
    created_at: datetime
    crop: str
    disease: str
    raw_class: str
    confidence: float
    confidence_state: str
    model_version: str
    processing_time_ms: float
    image_data_uri: Optional[str] = None
    top_predictions: List[TopPredictionItem] = []

class ScanHistoryListResponse(BaseModel):
    total: int
    scans: List[ScanHistoryItem]
