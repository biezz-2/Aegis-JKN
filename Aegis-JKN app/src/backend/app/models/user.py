from sqlalchemy import Column, String, Integer, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
import uuid
from src.backend.app.models.base import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True, nullable=False)
    permissions = Column(JSONB) # Use JSONB for flexible RBAC permissions

class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"))
