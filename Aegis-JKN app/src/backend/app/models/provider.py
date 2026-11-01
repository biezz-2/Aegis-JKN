from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
import uuid
from src.backend.app.models.base import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
