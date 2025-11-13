# controllers/auth.py
from fastapi import APIRouter, HTTPException, status, Form, Request
from pydantic import BaseModel
from typing import Dict, Optional

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


# --------- unified token endpoint (JSON or x-www-form-urlencoded) ---------
@router.post("/token", response_model=TokenResponse)
async def token_unified(
    request: Request,
    # If the client sends form-encoded, these will be present:
    grant_type: Optional[str] = Form(None),
    client_id: Optional[str] = Form(None),
    client_secret: Optional[str] = Form(None),
    scope: Optional[str] = Form(None),
) -> Dict:
    """
    Accepts:
      1) JSON:
         {"client_id":"...", "client_secret":"...", "subject":"ui"}
      2) Form-encoded OAuth:
         grant_type=client_credentials&client_id=...&client_secret=...&scope=mcp
    """
    ctype = request.headers.get("content-type", "").lower()

    # ---- FORM path (OAuth client_credentials) ----
    if "application/x-www-form-urlencoded" in ctype or grant_type or client_id or client_secret:
        if grant_type != "client_credentials":
            raise HTTPException(status_code=400, detail="Unsupported grant_type")
        if not (client_id and client_secret):
            raise HTTPException(status_code=400, detail="Missing client_id or client_secret")
        if not validate_client(client_id, client_secret):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid client credentials")

        acc = create_access_token("client-credentials", minutes=15)
        ref = create_refresh_token("client-credentials", days=30)
        return {"access_token": acc, "refresh_token": ref, "token_type": "bearer", "expires_in": 900}

    # ---- JSON path ----
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Expected JSON or x-www-form-urlencoded")

    try:
        tr = TokenRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    if not validate_client(tr.client_id, tr.client_secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid client credentials")

    acc = create_access_token(tr.subject, minutes=15)
    ref = create_refresh_token(tr.subject, days=30)
    return {"access_token": acc, "refresh_token": ref, "token_type": "bearer", "expires_in": 900}


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
