"""Role based access control for the Aegis-JKN API.

The module exposes the FastAPI dependencies :func:`get_current_user`,
:func:`require_permission` and :func:`require_role`, plus the static permission
matrix used by the API layer. Token validation itself lives in
:mod:`app.core.security.auth`; this module only maps a verified token (or the
payload already attached to ``request.state`` by the auth middleware) onto a
:class:`CurrentUser` and enforces the resulting role/permission rules.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set

from fastapi import Depends, Header, HTTPException, Request, status

from .auth import TokenPayload, TokenType, verify_token

class Role(str, Enum):
    VERIFIER = "Verifier"
    AUDITOR = "Auditor"
    ADMIN = "Admin"

class Permission(str, Enum):
    CLAIM_READ = "claim:read"
    CLAIM_VERIFY = "claim:verify"
    AUDIT_READ = "audit:read"
    SYSTEM_CONFIG = "system:config"
    USER_MANAGE = "user:manage"
    REPORT_EXPORT = "report:export"

# Permission Matrix
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.VERIFIER: {
        Permission.CLAIM_READ,
        Permission.CLAIM_VERIFY,
        Permission.REPORT_EXPORT,
    },
    Role.AUDITOR: {
        Permission.CLAIM_READ,
        Permission.AUDIT_READ,
        Permission.REPORT_EXPORT,
    },
    Role.ADMIN: {
        Permission.CLAIM_READ,
        Permission.CLAIM_VERIFY,
        Permission.AUDIT_READ,
        Permission.SYSTEM_CONFIG,
        Permission.USER_MANAGE,
        Permission.REPORT_EXPORT,
    },
}

class CurrentUser:
    """Represents the authenticated user for the request context"""
    def __init__(self, user_id: str, role: Role, token_payload: TokenPayload):
        self.id = user_id
        self.role = role
        self.payload = token_payload

#: RFC 6750 challenge returned with every 401 so clients know how to re-auth.
_UNAUTHORIZED_HEADERS: Dict[str, str] = {"WWW-Authenticate": "Bearer"}


def _as_role(value: Any) -> Optional[Role]:
    """Coerce ``value`` to a :class:`Role`, returning ``None`` when unknown."""
    if isinstance(value, Role):
        return value
    if isinstance(value, str):
        try:
            return Role(value)
        except ValueError:
            return None
    return None


def has_permission(role: Role, permission: Permission) -> bool:
    """Check if a role has a specific permission."""
    resolved = _as_role(role)
    if resolved is None:
        return False
    return permission in ROLE_PERMISSIONS.get(resolved, set())


def _unauthorized() -> HTTPException:
    """Build the 401 used for missing, malformed or unverifiable credentials."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers=dict(_UNAUTHORIZED_HEADERS),
    )


def _forbidden(detail: str) -> HTTPException:
    """Build the 403 used for an authenticated caller lacking the right role."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def _build_user(user_id: str, raw_role: Any, payload: TokenPayload) -> CurrentUser:
    """Build a :class:`CurrentUser`, rejecting unusable credentials.

    An unknown role is a ``403`` (the caller *is* authenticated, they simply
    hold a role this service does not implement). A refresh token is a ``401``:
    it is not an access credential and must never authorise an API request.
    """
    if getattr(payload, "token_type", TokenType.ACCESS) != TokenType.ACCESS:
        raise _unauthorized()

    role = _as_role(raw_role)
    if role is None:
        raise _forbidden(f"Invalid role: {raw_role!r}")

    return CurrentUser(user_id=user_id, role=role, token_payload=payload)


def _user_from_state(candidate: Any) -> Optional[CurrentUser]:
    """Normalise whatever ``AuthMiddleware`` stored on ``request.state.user``.

    The middleware attaches the verified :class:`TokenPayload` itself, but a
    pre-built :class:`CurrentUser` (or any duck-typed payload exposing ``sub``
    and ``role``) is accepted as well.
    """
    if isinstance(candidate, CurrentUser):
        return candidate
    if isinstance(candidate, TokenPayload):
        return _build_user(candidate.sub, candidate.role, candidate)

    subject = getattr(candidate, "sub", None)
    role = getattr(candidate, "role", None)
    if subject is None or role is None:
        return None
    return _build_user(subject, role, candidate)


async def get_current_user(
    request: Request,
    authorization: str | None = Header(default=None),
) -> CurrentUser:
    """Resolve the authenticated caller for the current request.

    Resolution order:

    1. ``request.state.user`` - already verified and attached by
       ``AuthMiddleware``. This is the normal path; it avoids decoding the same
       JWT twice per request.
    2. The ``Authorization: Bearer <token>`` header, so the dependency also
       works when the middleware is not installed (unit tests, sub-apps).

    A missing, malformed, expired or otherwise invalid credential raises
    ``401 Not authenticated`` with an RFC 6750 ``WWW-Authenticate: Bearer``
    challenge. A valid token whose role is not part of :class:`Role` raises
    ``403`` instead.
    """
    state_user = _user_from_state(getattr(request.state, "user", None))
    if state_user is not None:
        return state_user

    if not authorization:
        raise _unauthorized()

    scheme, _, credentials = authorization.partition(" ")
    token = credentials.strip()
    if scheme.lower() != "bearer" or not token:
        raise _unauthorized()

    try:
        payload = verify_token(token)
    except ValueError:
        # Expired, tampered with, or otherwise invalid token.
        raise _unauthorized() from None
    except Exception:
        # Defensive: a crypto/decoding blow-up must not surface as a 500.
        raise _unauthorized() from None

    return _build_user(payload.sub, payload.role, payload)

def require_permission(permission: Permission):
    """Dependency factory enforcing a single :class:`Permission`.

    Use it as a route-level guard::

        @router.get(
            "/claims",
            dependencies=[Depends(require_permission(Permission.CLAIM_READ))],
        )
        async def list_claims(): ...

    or bind it to a handler argument to also receive the authenticated user::

        user: CurrentUser = Depends(require_permission(Permission.CLAIM_VERIFY))
    """

    async def dependency(
        user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:
        if not has_permission(user.role, permission):
            raise _forbidden(f"Permission denied: {permission.value} required")
        return user

    return dependency


def require_role(*roles: Role):
    """Dependency factory enforcing that the caller holds one of ``roles``.

    Roles are normalised to :class:`Role`, so plain strings such as ``"Admin"``
    are accepted too. The guard raises ``ValueError`` when it is built with no
    role, or with a role that is not part of :class:`Role`, so a misconfigured
    route fails at import time instead of on the first request.
    """

    allowed: List[Role] = []
    for role in roles:
        resolved = _as_role(role)
        if resolved is None:
            raise ValueError(f"require_role() got an unknown role: {role!r}")
        if resolved not in allowed:
            allowed.append(resolved)

    if not allowed:
        raise ValueError("require_role() requires at least one role")

    allowed_set: Set[Role] = set(allowed)
    allowed_names = ", ".join(sorted(role.value for role in allowed))

    async def dependency(
        user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:
        current = _as_role(user.role)
        if current is None or current not in allowed_set:
            held = current.value if current is not None else repr(user.role)
            raise _forbidden(
                f"Role not permitted: '{held}' is not one of [{allowed_names}]"
            )
        return user

    return dependency
