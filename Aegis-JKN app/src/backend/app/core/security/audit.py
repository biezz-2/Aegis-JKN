import os
import json
import logging
import hashlib
import hmac
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Literal
from enum import Enum
from dataclasses import dataclass, asdict, field
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("audit")

class AuditAction(str, Enum):
    """Standardized audit actions"""
    # Authentication
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    LOGOUT = "LOGOUT"
    TOKEN_REFRESH = "TOKEN_REFRESH"
    TOKEN_REVOKED = "TOKEN_REVOKED"

    # Claims
    CLAIM_CREATE = "CLAIM_CREATE"
    CLAIM_READ = "CLAIM_READ"
    CLAIM_UPDATE = "CLAIM_UPDATE"
    CLAIM_DELETE = "CLAIM_DELETE"
    CLAIM_VERIFY = "CLAIM_VERIFY"
    CLAIM_REJECT = "CLAIM_REJECT"

    # Audit
    AUDIT_LOG_ACCESS = "AUDIT_LOG_ACCESS"
    AUDIT_REPORT_EXPORT = "AUDIT_REPORT_EXPORT"

    # System
    USER_CREATE = "USER_CREATE"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
    ROLE_ASSIGN = "ROLE_ASSIGN"
    CONFIG_CHANGE = "CONFIG_CHANGE"

    # Security
    PERMISSION_DENIED = "PERMISSION_DENIED"
    SUSPICIOUS_ACTIVITY = "SUSPICIOUS_ACTIVITY"

class AuditOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ERROR = "ERROR"

@dataclass
class Actor:
    """Actor performing the action"""
    id: str
    role: str
    ip: str
    user_agent: Optional[str] = None

@dataclass
class Resource:
    """Resource being accessed"""
    type: str
    id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditEvent:
    """Structured audit log entry"""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = ""
    actor: Actor = field(default_factory=lambda: Actor(id="anonymous", role="unknown", ip="unknown"))
    action: AuditAction = AuditAction.CLAIM_READ
    resource: Resource = field(default_factory=lambda: Resource(type="unknown", id="unknown"))
    changes: Dict[str, Any] = field(default_factory=dict)
    outcome: AuditOutcome = AuditOutcome.SUCCESS
    error_message: Optional[str] = None
    signature: str = ""  # HMAC for integrity

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(',', ':'), ensure_ascii=False)

class AuditLogger:
    """
    Audit logger with integrity protection.
    Logs are written to a secure sink (file, syslog, Elasticsearch, etc.)
    """
    def __init__(self):
        self.audit_key = os.getenv("AUDIT_HMAC_KEY", "").encode()
        self.log_file = os.getenv("AUDIT_LOG_FILE", "logs/audit.log")

        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Configure file handler
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setFormatter(logging.Formatter('%(message)s'))

        self.audit_logger = logging.getLogger("audit.events")
        self.audit_logger.setLevel(logging.INFO)
        self.audit_logger.addHandler(self.file_handler)
        self.audit_logger.propagate = False

    def _sign_event(self, event_json: str) -> str:
        """Generate HMAC signature for event integrity"""
        if not self.audit_key:
            return ""
        return hmac.new(self.audit_key, event_json.encode(), hashlib.sha256).hexdigest()

    def log(self, event: AuditEvent):
        """Log an audit event with integrity signature"""
        # Sign the event (excluding signature field)
        event_dict = event.to_dict()
        event_dict.pop('signature', None)
        event_json = json.dumps(event_dict, separators=(',', ':'), ensure_ascii=False)
        event.signature = self._sign_event(event_json)

        # Log the full event with signature
        self.audit_logger.info(event.to_json())

    def log_event(
        self,
        trace_id: str,
        actor: Actor,
        action: AuditAction,
        resource: Resource,
        changes: Dict[str, Any] = None,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        error_message: str = None
    ):
        """Convenience method to create and log an event"""
        event = AuditEvent(
            trace_id=trace_id,
            actor=actor,
            action=action,
            resource=resource,
            changes=changes or {},
            outcome=outcome,
            error_message=error_message
        )
        self.log(event)

# Global audit logger instance
_audit_logger = None

def get_audit_logger() -> AuditLogger:
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger

def log_audit_event(
    trace_id: str,
    actor: Actor,
    action: AuditAction,
    resource: Resource,
    changes: Dict[str, Any] = None,
    outcome: AuditOutcome = AuditOutcome.SUCCESS,
    error_message: str = None
):
    """Global function to log audit events"""
    get_audit_logger().log_event(
        trace_id=trace_id,
        actor=actor,
        action=action,
        resource=resource,
        changes=changes,
        outcome=outcome,
        error_message=error_message
    )

class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically log all HTTP requests for audit trail.
    """
    SENSITIVE_ENDPOINTS = {
        "/api/auth/login",
        "/api/auth/refresh",
        "/api/claims",
        "/api/users",
        "/api/audit",
        "/api/system",
    }

    def __init__(self, app):
        super().__init__(app)
        self.audit_logger = get_audit_logger()

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        trace_id = request.headers.get("X-Trace-ID", f"trace-{int(start_time * 1000)}")

        # Extract actor info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent")

        # Try to get user from token (if auth middleware ran first)
        user_id = "anonymous"
        user_role = "unknown"
        if hasattr(request.state, "user"):
            user_id = request.state.user.id
            user_role = request.state.user.role.value

        actor = Actor(
            id=user_id,
            role=user_role,
            ip=client_ip,
            user_agent=user_agent
        )

        # Process request
        response = await call_next(request)

        # Determine if this is a sensitive endpoint
        is_sensitive = any(
            request.url.path.startswith(path)
            for path in self.SENSITIVE_ENDPOINTS
        )

        # Log sensitive actions
        if is_sensitive or response.status_code >= 400:
            # Determine action from path/method
            action = self._infer_action(request)
            resource = Resource(
                type="endpoint",
                id=request.url.path,
                metadata={"method": request.method}
            )

            outcome = AuditOutcome.SUCCESS if response.status_code < 400 else AuditOutcome.FAILURE
            error_message = None if response.status_code < 400 else f"HTTP {response.status_code}"

            self.audit_logger.log_event(
                trace_id=trace_id,
                actor=actor,
                action=action,
                resource=resource,
                outcome=outcome,
                error_message=error_message
            )

        # Add trace ID to response headers
        response.headers["X-Trace-ID"] = trace_id
        return response

    def _infer_action(self, request: Request) -> AuditAction:
        """Infer audit action from request path and method"""
        path = request.url.path
        method = request.method

        if "/auth/login" in path:
            return AuditAction.LOGIN_SUCCESS if method == "POST" else AuditAction.LOGIN_FAILURE
        elif "/auth/refresh" in path:
            return AuditAction.TOKEN_REFRESH
        elif "/claims" in path:
            if method == "POST":
                return AuditAction.CLAIM_CREATE
            elif method in ("PUT", "PATCH"):
                if "verify" in path:
                    return AuditAction.CLAIM_VERIFY
                if "reject" in path:
                    return AuditAction.CLAIM_REJECT
                return AuditAction.CLAIM_UPDATE
            elif method == "DELETE":
                return AuditAction.CLAIM_DELETE
            return AuditAction.CLAIM_READ
        elif "/users" in path:
            if method == "POST":
                return AuditAction.USER_CREATE
            elif method in ("PUT", "PATCH"):
                return AuditAction.USER_UPDATE
            elif method == "DELETE":
                return AuditAction.USER_DELETE
            return AuditAction.CLAIM_READ  # fallback
        elif "/audit" in path:
            return AuditAction.AUDIT_LOG_ACCESS
        elif "/system" in path or "/config" in path:
            return AuditAction.CONFIG_CHANGE

        return AuditAction.CLAIM_READ

# Dependency to get current trace ID for manual audit logging
from fastapi import Request, Depends

def get_trace_id(request: Request) -> str:
    return request.headers.get("X-Trace-ID", "")