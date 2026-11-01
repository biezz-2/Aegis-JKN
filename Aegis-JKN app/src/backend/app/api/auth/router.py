"""Authentication API endpoints for Aegis-JKN."""
import time
from typing import Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from ...core.responses import APIResponse
from ...core.security.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    rotate_refresh_token,
    verify_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "Admin": ["read", "score", "audit", "export", "all"],
    "Auditor": ["read", "audit", "export"],
    "Verifier": ["read", "score"],
}


class LoginRequest(BaseModel):
    username: str = Field(..., description="User ID or username")
    password: str = Field(..., description="User password")
    role: Optional[str] = Field(default="Verifier", description="Requested role (Admin, Auditor, Verifier)")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="RS256 refresh token")


class UserProfile(BaseModel):
    id: str
    username: str
    role: str
    permissions: List[str]


class TokenResponseData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserProfile


@router.post("/login", response_model=APIResponse[TokenResponseData])
async def login(req: LoginRequest):
    """Authenticate user credentials and issue RS256 token pair."""
    # Development authentication mock; in production validate against user DB
    if not req.username or not req.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )

    # Resolve role and permissions
    role = req.role if req.role in ROLE_PERMISSIONS else "Verifier"
    permissions = ROLE_PERMISSIONS[role]

    access_token = create_access_token(
        subject=req.username,
        role=role,
        permissions=permissions,
    )
    refresh_token, _ = create_refresh_token(
        subject=req.username,
        role=role,
    )

    user = UserProfile(
        id=f"usr_{req.username}",
        username=req.username,
        role=role,
        permissions=permissions,
    )

    return APIResponse(
        success=True,
        message="Login successful",
        data=TokenResponseData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,
            user=user,
        ),
    )


@router.get("/validate", response_model=APIResponse[UserProfile])
async def validate_session(authorization: Optional[str] = Header(None)):
    """Validate bearer access token and return user profile."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token missing or malformed",
        )

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = verify_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
        )

    role = payload.role or "Verifier"
    permissions = ROLE_PERMISSIONS.get(role, ["read"])

    user = UserProfile(
        id=f"usr_{payload.sub}",
        username=payload.sub,
        role=role,
        permissions=permissions,
    )

    return APIResponse(
        success=True,
        message="Session valid",
        data=user,
    )


@router.post("/refresh", response_model=APIResponse[TokenResponseData])
async def refresh_session(req: RefreshRequest):
    """Rotate refresh token and issue a fresh access token."""
    try:
        new_access_token, new_refresh_token, payload = rotate_refresh_token(req.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token rotation failed: {str(e)}",
        )

    role = payload.role or "Verifier"
    permissions = ROLE_PERMISSIONS.get(role, ["read"])

    user = UserProfile(
        id=f"usr_{payload.sub}",
        username=payload.sub,
        role=role,
        permissions=permissions,
    )

    return APIResponse(
        success=True,
        message="Tokens refreshed",
        data=TokenResponseData(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=900,
            user=user,
        ),
    )
