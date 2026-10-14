from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.report_service import generate_pdf_report

router = APIRouter()

@router.get("/reports/{prediction_id}/pdf")
def download_scan_pdf(prediction_id: str, db: Session = Depends(get_db)):
    """
    Generates and streams a formal PDF diagnostic screening report for a prediction ID.
    """
    try:
        pdf_buffer = generate_pdf_report(prediction_id, db)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=AgroAI_Report_{prediction_id[:8]}.pdf"
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to generate PDF: {str(e)}")
