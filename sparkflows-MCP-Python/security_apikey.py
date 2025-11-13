# security_apikey.py
import os
from fastapi import HTTPException, status

def get_server_api_key() -> str:
    return os.getenv("MCP_API_KEY", "")

def validate_api_key(presented: str) -> None:
    server_key = get_server_api_key()
    if not server_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server API key not configured")
    if not presented or presented != server_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key")
