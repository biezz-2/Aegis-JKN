from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Shared base class for all models to avoid circular imports."""
    pass