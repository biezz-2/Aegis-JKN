"""Authentication and service-to-service (mTLS) middleware.

Both middlewares subclass Starlette's ``BaseHTTPMiddleware``. Exceptions raised
inside ``dispatch`` are not routed through FastAPI's exception handlers: a
raised ``HTTPException`` reaches the client as a bare 500. Every rejection is
therefore returned as an explicit ``JSONResponse`` with a JSON ``detail`` body.
"""

import logging
from typing import Dict, Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..core.security.auth import verify_token
from ..core.security.mtls import verify_mtls_request

logger = logging.getLogger(__name__)

#: Paths that are reachable without a bearer token.
public_paths = frozenset(
    {
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/openapi.json",
        "/docs/oauth2-redirect",
        "/health",
        "/metrics",
    }
)

#: Path prefixes that are always public in development mode.
public_path_prefixes = (
    "/api/auth/",
    "/api/report",
    "/api/graph",
    "/api/simulation",
    "/api/metrics",
    "/api/jobs",
    "/api/mcp",
)
#: Path prefixes that require a verified mTLS peer certificate.
mtls_protected_prefixes = ("/api/internal",)

#: Challenge header sent with bearer-token rejections (RFC 6750).
_BEARER_CHALLENGE = {"WWW-Authenticate": "Bearer"}


def is_public_path(path: str) -> bool:
    """Return ``True`` when ``path`` is served without a bearer token."""
    if path in public_paths:
        return True
    return any(path.startswith(prefix) for prefix in public_path_prefixes)


def _error(
    status_code: int,
    detail: str,
    headers: Optional[Dict[str, str]] = None,
) -> JSONResponse:
    """Build a JSON error response instead of raising ``HTTPException``."""
    return JSONResponse(
        {"detail": detail},
        status_code=status_code,
        headers=headers,
    )


class AuthMiddleware(BaseHTTPMiddleware):
    """Require a valid JWT for every non-public endpoint."""

    async def dispatch(self, request: Request, call_next):
        # CORS preflight requests never carry credentials.
        if request.method == "OPTIONS":
            return await call_next(request)

        # Health checks, API docs and the real auth routes stay reachable.
        if is_public_path(request.url.path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        scheme, _, credentials = auth_header.partition(" ")
        token = credentials.strip()

        if scheme.lower() != "bearer" or not token:
            return _error(
                401,
                "Missing or invalid authorization header",
                _BEARER_CHALLENGE,
            )

        try:
            payload = verify_token(token)
        except ValueError as exc:
            return _error(401, str(exc), _BEARER_CHALLENGE)
        except Exception:
            # Defensive: a verification blow-up must not become a 500.
            logger.exception("Unexpected failure while verifying bearer token")
            return _error(401, "Could not validate credentials", _BEARER_CHALLENGE)

        # Attach the verified payload (.sub, .role, .token_type) so downstream
        # dependencies can build the CurrentUser for RBAC checks.
        request.state.user = payload

        return await call_next(request)


class MTLSMiddleware(BaseHTTPMiddleware):
    """Enforce mTLS for service-to-service endpoints (``/api/internal``)."""

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        if not any(path.startswith(prefix) for prefix in mtls_protected_prefixes):
            return await call_next(request)

        try:
            identity = await verify_mtls_request(request)
        except HTTPException as exc:
            # verify_mtls_request() signals rejection by raising HTTPException;
            # translate it into a response instead of propagating it.
            return _error(401, str(exc.detail))
        except Exception:
            logger.exception("Unexpected failure during mTLS verification")
            return _error(500, "Internal mTLS verification error")

        if not identity:
            return _error(401, "mTLS authentication failed")

        request.state.service_identity = identity

        return await call_next(request)
