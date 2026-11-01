"""Standardized API responses for Aegis-JKN."""
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    success: bool = Field(..., description="Indicates if the request was successful")
    data: Optional[T] = Field(None, description="The actual response data")
    error: Optional[str] = Field(None, description="Error message if success is false")
    message: Optional[str] = Field(None, description="A human-readable status message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: Optional[str] = Field(None, description="Trace ID for request tracking")

class PaginationParams(BaseModel):
    """Standard pagination parameters."""
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

class PaginatedResponse(APIResponse[T], Generic[T]):
    """Response wrapper for lists of data with pagination."""
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    current_page: Optional[int] = None
    page_size: Optional[int] = None
