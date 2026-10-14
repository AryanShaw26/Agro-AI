import io
import json
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.lib.units import inch

from sqlalchemy.orm import Session
from app.models.db_models import ScanPrediction, Disease

def generate_pdf_report(prediction_id: str, db: Session) -> io.BytesIO:
    scan = db.query(ScanPrediction).filter_by(id=prediction_id).first()
    if not scan:
        raise ValueError(f"Scan record {prediction_id} not found")

    disease_info = db.query(Disease).filter_by(raw_class=scan.raw_class).first()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Styles
    forest_green = colors.HexColor("#1F694B")
    emerald = colors.HexColor("#2E8B67")
    charcoal = colors.HexColor("#1C231F")
    soft_sage = colors.HexColor("#E7F0EA")
    off_white = colors.HexColor("#F7F5EE")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=forest_green
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#6B756F")
    )

    heading2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=forest_green,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=charcoal
    )

    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )

    disclaimer_style = ParagraphStyle(
        "DocDisclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#B7791F")
    )

    story = []

    # Header
    story.append(Paragraph("AgroAI — Plant Disease Screening Report", title_style))
    story.append(Paragraph(f"Scan ID: {scan.id} | Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=forest_green, spaceBefore=0, spaceAfter=12))

    # Summary table
    status_color = "#1F694B" if scan.confidence_state == "confident" else "#B7791F"
    summary_data = [
        [Paragraph("<b>Crop:</b>", body_style), Paragraph(scan.crop, body_style),
         Paragraph("<b>Model Version:</b>", body_style), Paragraph(scan.model_version, body_style)],
        [Paragraph("<b>Condition:</b>", body_style), Paragraph(f"<b>{scan.disease}</b>", body_style),
         Paragraph("<b>Inference Time:</b>", body_style), Paragraph(f"{scan.processing_time_ms} ms", body_style)],
        [Paragraph("<b>Model Confidence:</b>", body_style), Paragraph(f"<font color='{status_color}'><b>{scan.confidence * 100:.1f}%</b> ({scan.confidence_state.title()})</font>", body_style),
         Paragraph("<b>Verification Source:</b>", body_style), Paragraph(disease_info.verified_source if disease_info else "Knowledge Base", body_style)]
    ]

    t_summary = Table(summary_data, colWidths=[1.3*inch, 2.2*inch, 1.4*inch, 2.3*inch])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), soft_sage),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, emerald),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 14))

    # Top predictions breakdown
    story.append(Paragraph("Top Model Probabilities", heading2_style))
    try:
        top_list = json.loads(scan.top_predictions_json)
        pred_table_data = [["Rank", "Candidate Condition", "Crop", "Confidence Probability"]]
        for i, item in enumerate(top_list, 1):
            pred_table_data.append([
                str(i),
                item.get("disease", ""),
                item.get("crop", ""),
                f"{float(item.get('confidence', 0)) * 100:.2f}%"
            ])
        t_pred = Table(pred_table_data, colWidths=[0.6*inch, 3.2*inch, 1.6*inch, 1.8*inch])
        t_pred.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), forest_green),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ]))
        story.append(t_pred)
    except Exception as e:
        story.append(Paragraph(f"Top predictions unavailable: {e}", body_style))

    story.append(Spacer(1, 14))

    # Verified Knowledge Section
    if disease_info:
        story.append(Paragraph("Verified Agricultural Knowledge", heading2_style))
        story.append(Paragraph(f"<b>Overview:</b> {disease_info.overview}", body_style))
        story.append(Spacer(1, 8))

        if disease_info.symptoms:
            story.append(Paragraph("<b>Known Symptoms:</b>", body_style))
            for sym in disease_info.symptoms:
                story.append(Paragraph(f"• {sym.symptom}", bullet_style))
            story.append(Spacer(1, 8))

        if disease_info.preventions:
            story.append(Paragraph("<b>Prevention & Management:</b>", body_style))
            for prev in disease_info.preventions:
                story.append(Paragraph(f"• {prev.prevention_step}", bullet_style))
            story.append(Spacer(1, 8))

        if disease_info.treatments:
            story.append(Paragraph("<b>Verified Treatment Options:</b>", body_style))
            for tr in disease_info.treatments:
                note = f" <i>(Caution: {tr.safety_note})</i>" if tr.safety_note else ""
                story.append(Paragraph(f"• <b>[{tr.treatment_type}]</b> {tr.description}{note}", bullet_style))
            story.append(Spacer(1, 8))

        if disease_info.safety_notes:
            story.append(Paragraph(f"<b>Safety Warning:</b> {disease_info.safety_notes}", disclaimer_style))
            story.append(Spacer(1, 8))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#D1D5DB"), spaceBefore=6, spaceAfter=8))
    
    # Disclaimer
    disclaimer_text = (
        "<b>LEGAL & AGRONOMIC DISCLAIMER:</b> This report is generated by AgroAI Model 1 (EfficientNet-B0) "
        "as a diagnostic screening aid. It is intended for informational and educational purposes only and does NOT "
        "constitute a certified agronomic diagnosis or definitive chemical prescription. Always consult certified "
        "local agricultural extension officers before applying chemical treatments. Follow all regional pesticide "
        "regulations and safety labels."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
