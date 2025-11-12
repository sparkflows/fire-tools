# controllers/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict

from security_jwt import (
    validate_client,
    create_access_token,
    create_refresh_token,
    decode_jwt,            # we'll use this for refresh verification
)

router = APIRouter(prefix="/auth", tags=["auth"])


# --------- models ---------
class TokenRequest(BaseModel):
    client_id: str
    client_secret: str
    subject: str = "user"   # who the token is for (e.g., "dhruv")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900   # seconds (15m)


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900


# --------- endpoints ---------
@router.post("/token", response_model=TokenResponse)
def token(req: TokenRequest) -> Dict:
    # Validate client credentials against env
    if not validate_client(req.client_id, req.client_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
        )
    acc = create_access_token(req.subject, minutes=15)
    ref = create_refresh_token(req.subject, days=30)
    return {
        "access_token": acc,
        "refresh_token": ref,
        "token_type": "bearer",
        "expires_in": 900,
    }


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(req: RefreshRequest) -> Dict:
    # Verify the refresh token and mint a new access token
    claims = decode_jwt(req.refresh_token, expect_typ="refresh")
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token missing subject",
        )
    acc = create_access_token(sub, minutes=15)
    return {"access_token": acc, "token_type": "bearer", "expires_in": 900}


# ---- optional: quick debug (masked) ----
@router.get("/debug")
def debug_creds():
    import os
    cid = os.getenv("MCP_CLIENT_ID", "")
    cs = os.getenv("MCP_CLIENT_SECRET", "")

    def mask(s: str) -> str:
        if not s:
            return ""
        return s[:4] + "..." + s[-4:] if len(s) > 8 else "***"

    return {
        "client_id_prefix": cid[:8],
        "client_id_masked": mask(cid),
        "client_secret_len": len(cs),
        "client_secret_masked": mask(cs),
    }
