from typing import List, Optional
from pydantic import BaseModel
from app.schemas.predict import TreatmentItem, ReferenceItem

class DiseaseListItem(BaseModel):
    id: str
    raw_class: str
    crop: str
    disease_name: str
    slug: str
    is_healthy: bool
    severity: Optional[str] = None
    overview: str
    verified_source: str

class DiseaseDetailResponse(BaseModel):
    id: str
    raw_class: str
    crop: str
    disease_name: str
    slug: str
    is_healthy: bool
    causal_agent: Optional[str] = None
    severity: Optional[str] = None
    overview: str
    safety_notes: Optional[str] = None
    verified_source: str
    symptoms: List[str] = []
    preventions: List[str] = []
    treatments: List[TreatmentItem] = []
    references: List[ReferenceItem] = []
