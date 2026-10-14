from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.models.db_models import Disease
from app.schemas.disease import DiseaseListItem, DiseaseDetailResponse
from app.schemas.predict import TreatmentItem, ReferenceItem

router = APIRouter()

@router.get("/diseases", response_model=List[DiseaseListItem])
def list_diseases(
    crop: Optional[str] = Query(None, description="Filter by crop name (e.g. Tomato, Apple)"),
    search: Optional[str] = Query(None, description="Search condition, causal agent, or symptom"),
    healthy_only: Optional[bool] = Query(None, description="Filter healthy classes"),
    db: Session = Depends(get_db)
):
    """
    Returns list of all supported 38 disease and healthy crop classes.
    """
    query = db.query(Disease)

    if crop:
        query = query.filter(Disease.crop.ilike(f"%{crop}%"))

    if healthy_only is not None:
        query = query.filter(Disease.is_healthy == healthy_only)

    if search:
        query = query.filter(
            or_(
                Disease.disease_name.ilike(f"%{search}%"),
                Disease.crop.ilike(f"%{search}%"),
                Disease.overview.ilike(f"%{search}%"),
                Disease.causal_agent.ilike(f"%{search}%")
            )
        )

    diseases = query.order_by(Disease.crop.asc(), Disease.disease_name.asc()).all()

    return [
        DiseaseListItem(
            id=d.id,
            raw_class=d.raw_class,
            crop=d.crop,
            disease_name=d.disease_name,
            slug=d.slug,
            is_healthy=d.is_healthy,
            severity=d.severity,
            overview=d.overview,
            verified_source=d.verified_source
        )
        for d in diseases
    ]


@router.get("/diseases/{slug}", response_model=DiseaseDetailResponse)
def get_disease_detail(slug: str, db: Session = Depends(get_db)):
    """
    Retrieves full verified knowledge base article for a specific disease by slug.
    """
    disease = db.query(Disease).filter_by(slug=slug).first()
    if not disease:
        # Try raw_class fallback
        disease = db.query(Disease).filter_by(raw_class=slug).first()

    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease record with slug '{slug}' not found in knowledge base."
        )

    return DiseaseDetailResponse(
        id=disease.id,
        raw_class=disease.raw_class,
        crop=disease.crop,
        disease_name=disease.disease_name,
        slug=disease.slug,
        is_healthy=disease.is_healthy,
        causal_agent=disease.causal_agent,
        severity=disease.severity,
        overview=disease.overview,
        safety_notes=disease.safety_notes,
        verified_source=disease.verified_source,
        symptoms=[s.symptom for s in disease.symptoms],
        preventions=[p.prevention_step for p in disease.preventions],
        treatments=[
            TreatmentItem(
                treatment_type=t.treatment_type,
                description=t.description,
                safety_note=t.safety_note
            )
            for t in disease.treatments
        ],
        references=[
            ReferenceItem(
                title=r.title,
                publisher=r.publisher,
                url=r.url
            )
            for r in disease.references
        ]
    )
