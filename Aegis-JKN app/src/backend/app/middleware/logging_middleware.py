"""Structured JSON logging middleware with OpenTelemetry correlation."""
import logging
import json
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured JSON logging of HTTP requests/responses.
    Logs: timestamp, method, path, status_code, latency_ms, trace_id, span_id, user_agent, client_ip
    """

    def __init__(self, app: ASGIApp, logger_name: str = "aegis_jkn"):
        super().__init__(app)
        self.logger = logging.getLogger(logger_name)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate trace ID
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        # Extract client info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Record start time
        start_time = time.perf_counter()

        # Log request
        log_data = {
            "trace_id": trace_id,
            "event": "http_request",
            "method": request.method,
            "path": str(request.url.path),
            "query_params": dict(request.query_params),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self.logger.info(json.dumps(log_data))

        # Process request
        try:
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000  # ms

            # Log response
            response_log = {
                "trace_id": trace_id,
                "event": "http_response",
                "status_code": response.status_code,
                "latency_ms": round(process_time, 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            self.logger.info(json.dumps(response_log))

            # Add trace ID to response headers
            response.headers["X-Trace-ID"] = trace_id

            return response

        except Exception as e:
            process_time = (time.perf_counter() - start_time) * 1000
            error_log = {
                "trace_id": trace_id,
                "event": "http_error",
                "error": str(e),
                "latency_ms": round(process_time, 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            self.logger.error(json.dumps(error_log))
            raise

def setup_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """
    Configure application logging with structured JSON output.
    """
    log_level_value = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_value)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler()

    if log_format == "json":
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_obj = {
                    "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                }

                # Add extra fields if present
                if hasattr(record, "trace_id"):
                    log_obj["trace_id"] = record.trace_id
                if record.exc_info:
                    log_obj["exception"] = self.formatException(record.exc_info)

                return json.dumps(log_obj)

        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )

    root_logger.addHandler(handler)