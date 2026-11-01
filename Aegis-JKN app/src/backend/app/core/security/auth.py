import os
import time
import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Literal
from enum import Enum

from jose import jwt, JWTError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Use a simple in-memory store for revoked refresh tokens
# In production, use Redis with TTL
_revoked_refresh_tokens: Dict[str, float] = {}  # token -> expiry timestamp
_active_refresh_tokens: Dict[str, Dict[str, Any]] = {}  # token -> {user_id, family_id, expires_at}


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload:
    """Decoded JWT payload structure"""
    def __init__(
        self,
        sub: str,          # User ID
        role: str,         # User role
        token_type: TokenType,
        exp: int,          # Expiry timestamp
        iat: int,          # Issued at timestamp
        jti: str,          # JWT ID (unique per token)
        family_id: Optional[str] = None,  # Token family for rotation tracking
        **kwargs
    ):
        self.sub = sub
        self.role = role
        self.token_type = token_type
        self.exp = exp
        self.iat = iat
        self.jti = jti
        self.family_id = family_id
        self.extra = kwargs

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenPayload":
        return cls(
            sub=data.get("sub", ""),
            role=data.get("role", ""),
            token_type=TokenType(data.get("type", "access")),
            exp=data.get("exp", 0),
            iat=data.get("iat", 0),
            jti=data.get("jti", ""),
            family_id=data.get("family_id"),
            **{k: v for k, v in data.items() if k not in {"sub", "role", "type", "exp", "iat", "jti", "family_id"}}
        )


# Key Management
_PRIVATE_KEY: Optional[bytes] = None
_PUBLIC_KEY: Optional[bytes] = None


def _load_or_generate_keys():
    """Load RSA keys from environment or generate new ones for development."""
    global _PRIVATE_KEY, _PUBLIC_KEY

    private_key_pem = os.getenv("JWT_PRIVATE_KEY")
    public_key_pem = os.getenv("JWT_PUBLIC_KEY")

    if private_key_pem and public_key_pem:
        _PRIVATE_KEY = private_key_pem.encode()
        _PUBLIC_KEY = public_key_pem.encode()
    else:
        # Generate keys for development
        # In production, these MUST be loaded from secure storage (Vault)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        _PRIVATE_KEY = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key = private_key.public_key()
        _PUBLIC_KEY = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        print("WARNING: Using auto-generated RSA keys. Set JWT_PRIVATE_KEY and JWT_PUBLIC_KEY in production!")


def get_private_key() -> bytes:
    if _PRIVATE_KEY is None:
        _load_or_generate_keys()
    return _PRIVATE_KEY


def get_public_key() -> bytes:
    if _PUBLIC_KEY is None:
        _load_or_generate_keys()
    return _PUBLIC_KEY


# Token Configuration
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
ALGORITHM = "RS256"
ISSUER = "aegis-jkn"


def create_access_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
    **extra_claims
) -> str:
    """
    Create a short-lived access token (RS256).
    """
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": subject,
        "role": role,
        "type": TokenType.ACCESS.value,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
        "iss": ISSUER,
        **extra_claims
    }

    return jwt.encode(payload, get_private_key(), algorithm=ALGORITHM)


def create_refresh_token(
    subject: str,
    role: str,
    family_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a long-lived refresh token with rotation support.
    """
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    jti = str(uuid.uuid4())
    fam_id = family_id or str(uuid.uuid4())

    payload = {
        "sub": subject,
        "role": role,
        "type": TokenType.REFRESH.value,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": jti,
        "family_id": fam_id,
        "iss": ISSUER,
    }

    token = jwt.encode(payload, get_private_key(), algorithm=ALGORITHM)

    # Store for rotation tracking
    _active_refresh_tokens[jti] = {
        "user_id": subject,
        "family_id": fam_id,
        "expires_at": expire.timestamp(),
        "revoked": False
    }

    return token


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.
    """
    try:
        payload = jwt.decode(
            token,
            get_public_key(),
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            options={"verify_aud": False}
        )
        return TokenPayload.from_dict(payload)
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def verify_token(token: str) -> TokenPayload:
    """
    Verify a token is valid and not revoked.
    """
    payload = decode_token(token)

    # Check if access token is expired
    if payload.exp < time.time():
        raise ValueError("Token expired")

    # For refresh tokens, check revocation
    if payload.token_type == TokenType.REFRESH:
        if payload.jti in _revoked_refresh_tokens:
            # Check if it's a family attack (reuse of revoked token)
            family_tokens = [
                t for t, data in _active_refresh_tokens.items()
                if data.get("family_id") == payload.family_id and data.get("revoked")
            ]
            if len(family_tokens) > 0:
                # Token reuse detected - revoke entire family
                revoke_token_family(payload.family_id)
                raise ValueError("Token reuse detected - security breach")
            raise ValueError("Token revoked")

    return payload


def revoke_refresh_token(jti: str, family_id: str = None) -> bool:
    """
    Revoke a specific refresh token.
    If family_id provided, marks it for rotation tracking.
    """
    if jti in _active_refresh_tokens:
        _active_refresh_tokens[jti]["revoked"] = True
        _revoked_refresh_tokens[jti] = _active_refresh_tokens[jti]["expires_at"]
        return True
    return False


def revoke_token_family(family_id: str):
    """
    Revoke all tokens in a family (used when token reuse is detected).
    """
    now = time.time()
    for jti, data in _active_refresh_tokens.items():
        if data.get("family_id") == family_id and not data.get("revoked"):
            data["revoked"] = True
            _revoked_refresh_tokens[jti] = data["expires_at"]

    # In production: Also invalidate all access tokens for this user
    # This would require a token blacklist in Redis


def rotate_refresh_token(refresh_token: str) -> Dict[str, str]:
    """
    Rotate a refresh token: revoke old, issue new pair.
    Returns new access_token and refresh_token.
    """
    payload = verify_token(refresh_token)

    if payload.token_type != TokenType.REFRESH:
        raise ValueError("Invalid token type for rotation")

    # Revoke the used refresh token
    revoke_refresh_token(payload.jti, payload.family_id)

    # Create new token pair (same family for rotation tracking)
    new_access = create_access_token(payload.sub, payload.role)
    new_refresh = create_refresh_token(payload.sub, payload.role, family_id=payload.family_id)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }


def cleanup_expired_tokens():
    """
    Clean up expired tokens from memory stores.
    Should be run periodically (e.g., every hour).
    """
    now = time.time()

    # Clean revoked tokens
    expired_revoked = [jti for jti, exp in _revoked_refresh_tokens.items() if exp < now]
    for jti in expired_revoked:
        del _revoked_refresh_tokens[jti]

    # Clean active tokens
    expired_active = [jti for jti, data in _active_refresh_tokens.items() if data["expires_at"] < now]
    for jti in expired_active:
        del _active_refresh_tokens[jti]


# Initialize keys on module load
_load_or_generate_keys()