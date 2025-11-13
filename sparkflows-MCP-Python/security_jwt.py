# security_jwt.py
import os
import datetime as dt
from typing import Optional, Tuple, Dict, Any

import jwt  # PyJWT
from fastapi import Header, HTTPException, status

_ALG = "HS256"

def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)

def _get_iss() -> str:
    return os.getenv("MCP_JWT_ISS", "sparkflows-mcp").strip()

def _get_aud() -> str:
    return os.getenv("MCP_JWT_AUD", "mcp-clients").strip()

def _get_secret() -> str:
    s = os.getenv("MCP_JWT_SECRET", "").strip()
    if not s:
        raise RuntimeError("MCP_JWT_SECRET not set")
    return s

def validate_client(client_id: str, client_secret: str) -> bool:
    """
    Read the expected client id/secret from ENV at request-time
    so you can rotate them without restarting (still restart recommended).
    """
    expected_id = os.getenv("MCP_CLIENT_ID", "").strip()
    expected_secret = os.getenv("MCP_CLIENT_SECRET", "").strip()
    return bool(
        expected_id and expected_secret
        and client_id == expected_id
        and client_secret == expected_secret
    )

def create_access_token(sub: str, minutes: int = 15) -> str:
    iat = _now()
    exp = iat + dt.timedelta(minutes=minutes)
    payload = {
        "iss": _get_iss(),
        "aud": _get_aud(),
        "sub": sub,
        "iat": int(iat.timestamp()),
        "exp": int(exp.timestamp()),
        "typ": "access",
    }
    return jwt.encode(payload, _get_secret(), algorithm=_ALG)

def create_refresh_token(sub: str, days: int = 30) -> str:
    iat = _now()
    exp = iat + dt.timedelta(days=days)
    payload = {
        "iss": _get_iss(),
        "aud": _get_aud(),
        "sub": sub,
        "iat": int(iat.timestamp()),
        "exp": int(exp.timestamp()),
        "typ": "refresh",
    }
    return jwt.encode(payload, _get_secret(), algorithm=_ALG)

def decode_jwt(token: str, expect_typ: Optional[str] = None) -> Dict[str, Any]:
    try:
        claims = jwt.decode(
            token,
            _get_secret(),
            algorithms=[_ALG],
            audience=_get_aud(),
            issuer=_get_iss(),
            options={"require": ["iss", "aud", "sub", "exp"]}
        )
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")

    if expect_typ and claims.get("typ") != expect_typ:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    return claims

def require_access_token(Authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = Authorization[len("Bearer "):].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return decode_jwt(token, expect_typ="access")

def verify_bearer_token(token: str) -> str:
    """
    Validates a JWT *access* token and returns the subject ('sub').
    Raises HTTP 401 if invalid/expired/wrong type.
    """
    try:
        claims = decode_jwt(token, expect_typ="access")  # you already have decode_jwt(...)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid bearer token: {e}")
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid bearer token: missing subject")
    return sub