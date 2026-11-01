from sqlalchemy import Column, String, Float, ForeignKey, DateTime, UUID, Index
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
import uuid
from src.backend.app.models.base import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(String, unique=True, nullable=False, index=True)
    patient_id = Column(PGUUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    provider_id = Column(PGUUID(as_uuid=True), ForeignKey("providers.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String)
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Explicit B-Tree index for claim_id (handled by index=True)
