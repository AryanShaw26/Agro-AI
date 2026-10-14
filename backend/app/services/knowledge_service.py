from typing import Optional
from sqlalchemy.orm import Session
from app.models.db_models import Disease
from app.schemas.predict import KnowledgeResponse, TreatmentItem, ReferenceItem

class KnowledgeService:
    @staticmethod
    def get_by_raw_class(db: Session, raw_class: str) -> KnowledgeResponse:
        disease = db.query(Disease).filter_by(raw_class=raw_class).first()
        if not disease:
            # Fallback check by crop / disease
            return KnowledgeResponse(
                available=False,
                overview="Verified agricultural guidance is currently not available for this condition in our database."
            )

        return KnowledgeResponse(
            available=True,
            overview=disease.overview,
            causal_agent=disease.causal_agent,
            severity=disease.severity,
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

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Disease]:
        return db.query(Disease).filter_by(slug=slug).first()

knowledge_service = KnowledgeService()
