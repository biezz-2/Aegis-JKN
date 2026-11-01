from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.backend.app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    entity_id = Column(String, index=True)
    action = Column(String, nullable=False)
    user_id = Column(String, index=True)
    details = Column(JSONB, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # GIN Index for JSONB efficiency
    __table_args__ = (
        Index("idx_audit_details", "details", postgresql_using="gin"),
    )
