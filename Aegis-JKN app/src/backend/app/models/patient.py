from sqlalchemy import Column, String, Date, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
import uuid
from src.backend.app.models.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    dob = Column(Date)
    gender = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
