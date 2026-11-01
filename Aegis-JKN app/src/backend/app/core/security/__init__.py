"""
Security module for Aegis-JKN.
Provides authentication, authorization, secrets management, mTLS, and audit logging.
"""

from .auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
    TokenPayload,
    TokenType,
)
from .rbac import (
    Role,
    Permission,
    ROLE_PERMISSIONS,
    has_permission,
    require_permission,
    get_current_user,
    CurrentUser,
)
from .vault import VaultClient, get_vault_client, load_secrets_from_vault
from .mtls import (
    verify_client_certificate,
    extract_service_identity,
    MTLSError,
)
from .audit import (
    AuditEvent,
    AuditAction,
    AuditOutcome,
    log_audit_event,
    AuditMiddleware,
)

__all__ = [
    # Auth
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "decode_token",
    "TokenPayload",
    "TokenType",
    # RBAC
    "Role",
    "Permission",
    "ROLE_PERMISSIONS",
    "has_permission",
    "require_permission",
    "get_current_user",
    "CurrentUser",
    # Vault
    "VaultClient",
    "get_vault_client",
    "load_secrets_from_vault",
    # mTLS
    "verify_client_certificate",
    "extract_service_identity",
    "MTLSError",
    # Audit
    "AuditEvent",
    "AuditAction",
    "AuditOutcome",
    "log_audit_event",
    "AuditMiddleware",
]