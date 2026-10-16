from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TopPredictionItem(BaseModel):
    crop: str
    disease: str
    confidence: float
    is_healthy: bool
    slug: str
    raw_class: Optional[str] = None

class TreatmentItem(BaseModel):
    treatment_type: str
    description: str
    safety_note: Optional[str] = None

class ReferenceItem(BaseModel):
    title: str
    publisher: str
    url: Optional[str] = None

class KnowledgeResponse(BaseModel):
    available: bool
    overview: Optional[str] = None
    causal_agent: Optional[str] = None
    severity: Optional[str] = None
    safety_notes: Optional[str] = None
    verified_source: Optional[str] = None
    symptoms: List[str] = []
    preventions: List[str] = []
    treatments: List[TreatmentItem] = []
    references: List[ReferenceItem] = []

class GradCAMMetadata(BaseModel):
    available: bool
    target_class: Optional[str] = None
    target_class_index: Optional[int] = None
    overlay_url: Optional[str] = None
    heatmap_url: Optional[str] = None
    overlay_base64: Optional[str] = None
    heatmap_base64: Optional[str] = None
    disclaimer: Optional[str] = "AI explanation of convolutional attention — not diagnostic proof of disease."

class PredictionResponse(BaseModel):
    prediction_id: str
    crop: str
    disease: str
    confidence: float
    confidence_state: str  # "confident" or "uncertain"
    is_healthy: bool
    raw_class: str
    slug: str
    model_version: str
    processing_time_ms: float
    top_predictions: List[TopPredictionItem]
    knowledge: KnowledgeResponse
    gradcam: Optional[GradCAMMetadata] = None
    gradcam_image: Optional[str] = None  # Backward-compatible overlay field
    image_preview_url: Optional[str] = None
