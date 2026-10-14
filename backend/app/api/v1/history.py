import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.db_models import ScanPrediction
from app.schemas.history import ScanHistoryListResponse, ScanHistoryItem
from app.schemas.predict import TopPredictionItem

router = APIRouter()

@router.get("/history", response_model=ScanHistoryListResponse)
def get_scan_history(
    crop: Optional[str] = Query(None, description="Filter by crop"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Returns paginated list of past scan predictions.
    """
    query = db.query(ScanPrediction)
    if crop:
        query = query.filter(ScanPrediction.crop.ilike(f"%{crop}%"))

    total = query.count()
    records = query.order_by(ScanPrediction.created_at.desc()).offset(offset).limit(limit).all()

    items = []
    for r in records:
        top_preds = []
        try:
            raw_top = json.loads(r.top_predictions_json)
            top_preds = [
                TopPredictionItem(
                    crop=p["crop"],
                    disease=p["disease"],
                    confidence=p["confidence"],
                    is_healthy=p["is_healthy"],
                    slug=p["slug"]
                )
                for p in raw_top
            ]
        except Exception:
            pass

        items.append(
            ScanHistoryItem(
                id=r.id,
                created_at=r.created_at,
                crop=r.crop,
                disease=r.disease,
                raw_class=r.raw_class,
                confidence=r.confidence,
                confidence_state=r.confidence_state,
                model_version=r.model_version,
                processing_time_ms=r.processing_time_ms,
                image_data_uri=r.image_data_uri,
                top_predictions=top_preds
            )
        )

    return ScanHistoryListResponse(total=total, scans=items)


@router.delete("/history/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan_record(scan_id: str, db: Session = Depends(get_db)):
    """
    Deletes a scan prediction record from history.
    """
    scan = db.query(ScanPrediction).filter_by(id=scan_id).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan record not found")
    db.delete(scan)
    db.commit()
    return None
