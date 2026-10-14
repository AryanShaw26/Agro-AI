import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    raw_class = Column(String(128), unique=True, index=True, nullable=False)
    crop = Column(String(64), index=True, nullable=False)
    disease_name = Column(String(128), index=True, nullable=False)
    slug = Column(String(128), unique=True, index=True, nullable=False)
    is_healthy = Column(Boolean, default=False)
    overview = Column(Text, nullable=False)
    causal_agent = Column(String(128), nullable=True)
    severity = Column(String(64), nullable=True)
    safety_notes = Column(Text, nullable=True)
    verified_source = Column(String(256), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    symptoms = relationship("DiseaseSymptom", back_populates="disease", cascade="all, delete-orphan", order_by="DiseaseSymptom.order")
    preventions = relationship("DiseasePrevention", back_populates="disease", cascade="all, delete-orphan", order_by="DiseasePrevention.order")
    treatments = relationship("DiseaseTreatment", back_populates="disease", cascade="all, delete-orphan", order_by="DiseaseTreatment.order")
    references = relationship("DiseaseReference", back_populates="disease", cascade="all, delete-orphan")


class DiseaseSymptom(Base):
    __tablename__ = "disease_symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(String(64), ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False)
    symptom = Column(Text, nullable=False)
    order = Column(Integer, default=0)

    disease = relationship("Disease", back_populates="symptoms")


class DiseasePrevention(Base):
    __tablename__ = "disease_prevention"

    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(String(64), ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False)
    prevention_step = Column(Text, nullable=False)
    order = Column(Integer, default=0)

    disease = relationship("Disease", back_populates="preventions")


class DiseaseTreatment(Base):
    __tablename__ = "disease_treatments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(String(64), ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False)
    treatment_type = Column(String(64), nullable=False)  # e.g., "Cultural / Mechanical", "Biological / Organic", "Chemical"
    description = Column(Text, nullable=False)
    safety_note = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    disease = relationship("Disease", back_populates="treatments")


class DiseaseReference(Base):
    __tablename__ = "disease_references"

    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(String(64), ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    publisher = Column(String(128), nullable=False)
    url = Column(String(512), nullable=True)

    disease = relationship("Disease", back_populates="references")


class ScanPrediction(Base):
    __tablename__ = "scans"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    crop = Column(String(64), index=True, nullable=False)
    disease = Column(String(128), index=True, nullable=False)
    raw_class = Column(String(128), nullable=False)
    confidence = Column(Float, nullable=False)
    confidence_state = Column(String(32), nullable=False)  # "confident" or "uncertain"
    top_predictions_json = Column(Text, nullable=False)
    image_data_uri = Column(Text, nullable=True)
    model_version = Column(String(64), nullable=False)
    processing_time_ms = Column(Float, nullable=False)

