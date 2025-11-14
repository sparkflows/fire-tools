import os
from typing import Any, Dict, Optional, Union

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from mysql_mcp_service import (
    get_tools_list,
    handle_tool_call,
    get_initialize_response,
)

router = APIRouter()

# We’ll still read it at module import, but _verify_api_key will
# *require* that it is set and non-empty.
API_KEY = os.getenv("MCP_API_KEY")


class JSONRPCRequest(BaseModel):
    jsonrpc: Union[str, int, None] = "2.0"
    id: Union[str, int, None] = None
    method: str
    params: Optional[Dict[str, Any]] = None


def _extract_api_key_from_headers(request: Request) -> Optional[str]:
    """
    Try common patterns:
      - Authorization: Bearer <token>
      - Authorization: <token>
      - X-API-Key: <token>
    """
    auth = request.headers.get("authorization")
    if auth:
        parts = auth.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1].strip()
        return auth.strip()

    x_api_key = request.headers.get("x-api-key")
    if x_api_key:
        return x_api_key.strip()

    return None


def _verify_api_key(request: Request) -> None:
    """
    Require MCP_API_KEY and require that at least one header value matches it.
    """
    # 1) Ensure server is configured
    if not API_KEY:
        # Hard fail if the env var is not set – auth is mandatory
        raise HTTPException(
            status_code=500,
            detail="MCP_API_KEY environment variable is not set",
        )

    # 2) Try normal patterns first
    incoming = _extract_api_key_from_headers(request)
    if incoming and incoming == API_KEY:
        return

    # 3) Fallback: accept the key if it appears as the *value* of any header.
    #    (still requires an exact match to API_KEY)
    for _, value in request.headers.items():
        if value.strip() == API_KEY:
            return

    # 4) No match found → unauthorized
    raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/rpc")
async def rpc_handler(http_request: Request, request: JSONRPCRequest) -> Dict[str, Any]:
    # ---- API key check ----
    _verify_api_key(http_request)

    response: Dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": request.id if request.id is not None else 1,
    }

    try:
        method = request.method

        if method == "tools/list":
            response["result"] = get_tools_list()

        elif method == "tools/call":
            if request.params is None:
                raise ValueError("Missing params for tools/call")
            response["result"] = handle_tool_call(request.params)

        elif method == "initialize":
            response["result"] = get_initialize_response()

        else:
            response["error"] = {
                "code": -32601,
                "message": f"Method not found: {method}",
            }

    except HTTPException:
        # Let 4xx / 5xx from _verify_api_key bubble up unchanged
        raise
    except Exception as e:
        response["error"] = {
            "code": -32603,
            "message": f"Internal error: {e}",
        }

    return response
