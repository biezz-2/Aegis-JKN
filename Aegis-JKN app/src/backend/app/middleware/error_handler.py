"""Global error handling and exception mapping."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
import logging
import traceback
from datetime import datetime
from ..core.responses import APIResponse

logger = logging.getLogger("aegis_jkn")

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler to ensure all errors follow the APIResponse format.
    """
    trace_id = request.state.trace_id if hasattr(request.state, "trace_id") else "unknown"

    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        detail = exc.detail
    elif isinstance(exc, ValidationError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = str(exc.errors())
    else:
        # Log unexpected internal server errors
        logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = "An unexpected internal server error occurred."

    response_body = APIResponse(
        success=False,
        error=detail,
        message="An error occurred while processing your request.",
        trace_id=trace_id
    ).dict()

    return JSONResponse(
        status_code=status_code,
        content=response_body
    )
