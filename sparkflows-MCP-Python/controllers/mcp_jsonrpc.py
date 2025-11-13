# controllers/mcp_jsonrpc.py
from fastapi import APIRouter, Request, Header, HTTPException, status
from typing import Any, Dict, List, Optional, Tuple
import json

from services.mysql_mcp_service import MySqlMcpService
from security_jwt import verify_bearer_token
from security_apikey import validate_api_key

router = APIRouter()
svc = MySqlMcpService()

# ---------------------------- AUTH HELPERS ----------------------------

async def _auth_from_headers_or_body(
    req: Request,
    authorization: Optional[str],
    x_api_key: Optional[str],
    x_token: Optional[str],
):
    """
    Accept auth via (in order of precedence):
      1) Headers: Authorization: Bearer|Token <value>, X-API-Key, X-Token
      2) Body (top-level or under params): password | token | apiKey | apikey | api_key
      3) Query: ?token=... | ?api_key=... | ?apikey=...
    """

    # 1) Headers first
    if authorization:
        parts = authorization.split()
        if len(parts) == 2:
            scheme, cred = parts[0].lower(), parts[1]
            if scheme == "bearer":
                # Try JWT; if invalid, treat as API key
                try:
                    verify_bearer_token(cred)  # will raise if invalid
                    return {"auth": "bearer"}
                except Exception:
                    validate_api_key(cred)     # will raise if invalid
                    return {"auth": "api_key"}
            if scheme == "token":
                validate_api_key(cred)
                return {"auth": "api_key"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header"
        )

    if x_api_key:
        validate_api_key(x_api_key); return {"auth": "api_key"}
    if x_token:
        validate_api_key(x_token);   return {"auth": "api_key"}

    # 2) Body fields (matches UI test connection which sends password in body)
    body = {}
    try:
        body = await req.json()
    except Exception:
        body = {}

    def pick_from(mapping: Dict[str, Any]) -> Optional[str]:
        if not isinstance(mapping, dict):
            return None
        for k in ("password", "token", "apiKey", "apikey", "api_key"):
            v = mapping.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return None

    # top-level body
    v = pick_from(body)
    if v:
        validate_api_key(v); return {"auth": "api_key"}

    # nested under params
    params = body.get("params") if isinstance(body, dict) else None
    v = pick_from(params) if isinstance(params, dict) else None
    if v:
        validate_api_key(v); return {"auth": "api_key"}

    # 3) Query params (?token= / ?api_key= / ?apikey=)
    qp = req.query_params
    for qk in ("token", "api_key", "apikey"):
        qv = qp.get(qk)
        if isinstance(qv, str) and qv.strip():
            validate_api_key(qv.strip())
            return {"auth": "api_key"}

    # Nothing worked
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth")

# ---------------------------- TOOL DESCRIPTORS ----------------------------

def _tool_entry(
    name: str,
    description: str,
    properties: Dict[str, Any],
    required: List[str],
) -> Dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "tool_name": {"type": "string"},
                "status": {"type": "string"},
                "result": {"type": "object"},
                "next_steps": {"type": "object"},
            },
            "required": ["tool_name", "status", "result", "next_steps"],
        },
    }

def _ok_content(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": False}

def _err_content(msg: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Error: {msg}"}], "isError": True}

def _tools_list() -> Dict[str, Any]:
    tools: List[Dict[str, Any]] = []

    # Resource-backed (served by MySqlMcpService)
    tools.append(_tool_entry("createWorkflow",
        "Create workflow - returns the workflow JSON", {}, []))
    tools.append(_tool_entry("LegoblockXMLParser",
        "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)", {}, []))
    tools.append(_tool_entry("LegoblockXMLMapping",
        "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)", {}, []))
    tools.append(_tool_entry("createPipelineNode",
        "Create pipeline node - returns the pipeline node JSON", {}, []))
    tools.append(_tool_entry("createWorkflowNode",
        "Create workflow node - returns the workflow node JSON", {}, []))

    # Constructed examples
    tools.append(_tool_entry("CreateExtractionLegoBlock",
        "Create an extraction lego block by combining 2 strings",
        {
            "first_string": {"type": "string", "description": "First string"},
            "second_string": {"type": "string", "description": "Second string"},
        },
        ["first_string", "second_string"]
    ))

    tools.append(_tool_entry("logoblockXMl",
        "Create a small XML block descriptor",
        {
            "ClusterId": {"type": "string", "description": "Cluster ID"},
            "StepName": {"type": "string", "description": "Step name"},
            "deploy-mode": {"type": "string", "description": "Deployment mode (cluster/client)"},
        },
        ["ClusterId", "StepName", "deploy-mode"]
    ))

    tools.append(_tool_entry("ReadCSV",
        "Read CSV file from the specified path",
        {"path": {"type": "string", "description": "Path to the CSV file to read"}},
        ["path"]
    ))

    return {"tools": tools}

def _initialize() -> Dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": True},
            "sampling": {"enabled": True},
            "prompts": {"enabled": False},
            "resources": {"enabled": False},
        },
        "serverInfo": {
            "name": "workflow-mcp-server",
            "version": "1.0.0",
            "description": "Workflow and pipeline management MCP server (Python)",
        },
    }

def _call_tool(name: str, arguments: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        # Resource-backed
        if name == "createWorkflow":
            return True, svc.createWorkflow()
        if name == "LegoblockXMLParser":
            return True, svc.LegoblockXMLParser()
        if name == "LegoblockXMLMapping":
            return True, svc.LegoblockXMLMapping()
        if name == "createPipelineNode":
            return True, svc.createPipelineNode()
        if name == "createWorkflowNode":
            return True, svc.createWorkflowNode()

        # Constructed
        if name == "CreateExtractionLegoBlock":
            a = arguments or {}
            s1 = a.get("first_string", "")
            s2 = a.get("second_string", "")
            if not s1 or not s2:
                raise ValueError("Both first_string and second_string are required.")
            result = {
                "tool_name": "CreateExtractionLegoBlock",
                "status": "success",
                "result": {"combined": f"{s1}{s2}"},
                "next_steps": {},
            }
            return True, json.dumps(result, ensure_ascii=False, indent=2)

        if name == "logoblockXMl":
            a = arguments or {}
            cluster_id = a["ClusterId"]
            step_name = a["StepName"]
            deploy_mode = a["deploy-mode"]
            result = {
                "tool_name": "logoblockXMl",
                "status": "success",
                "result": {
                    "clusterId": cluster_id,
                    "stepName": step_name,
                    "deployMode": deploy_mode,
                },
                "next_steps": {},
            }
            return True, json.dumps(result, ensure_ascii=False, indent=2)

        if name == "ReadCSV":
            a = arguments or {}
            path = a["path"]
            result = {
                "tool_name": "ReadCSV",
                "status": "success",
                "result": {"path": path, "format": "csv"},
                "next_steps": {},
            }
            return True, json.dumps(result, ensure_ascii=False, indent=2)

        return False, f"Tool not found: {name}"

    except KeyError as e:
        return False, f"Missing required argument: {e}"
    except Exception as e:
        return False, str(e)

# ---------------------------- JSON-RPC CORE ----------------------------

async def _handle_json_rpc(req: Request) -> Dict[str, Any]:
    body = await req.json()
    method = body.get("method")
    _id = body.get("id")
    params = body.get("params", {})

    response: Dict[str, Any] = {"id": _id, "jsonrpc": "2.0"}

    try:
        if method == "tools/list":
            response["result"] = _tools_list()
        elif method == "initialize":
            response["result"] = _initialize()
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            ok, payload = _call_tool(name, arguments)
            response["result"] = _ok_content(payload) if ok else _err_content(payload)
        else:
            response["error"] = {"code": -32601, "message": "Method not found"}
    except Exception as e:
        response["error"] = {"code": -32000, "message": str(e)}

    return response

# ---------------------------- ROUTES ----------------------------

@router.post("/")
async def root_entrypoint(
    req: Request,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str]    = Header(None, alias="X-API-Key"),
    x_token: Optional[str]      = Header(None, alias="X-Token"),
):
    await _auth_from_headers_or_body(req, authorization, x_api_key, x_token)
    return await _handle_json_rpc(req)

@router.post("/mcp/rpc")
@router.post("/mcp/rpc/")
async def rpc_entrypoint(
    req: Request,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str]    = Header(None, alias="X-API-Key"),
    x_token: Optional[str]      = Header(None, alias="X-Token"),
):
    await _auth_from_headers_or_body(req, authorization, x_api_key, x_token)
    return await _handle_json_rpc(req)

# Helpful debug endpoint (no auth) — remove if you don’t want this exposed
@router.post("/debug/echo")
async def debug_echo(req: Request):
    headers = {k.lower(): v for k, v in req.headers.items()}
    body = {}
    try:
        body = await req.json()
    except Exception:
        body = {}

    def keyinfo(mapping: Dict[str, Any], key: str):
        v = mapping.get(key)
        if isinstance(v, str):
            s = v.strip()
            return {"len": len(s), "sha256_8": __import__("hashlib").sha256(s.encode()).hexdigest()[:8]}
        return None

    params = body.get("params") if isinstance(body, dict) else None
    return {
        "headers": {
            "has_authorization": "authorization" in headers,
            "has_x_api_key": "x-api-key" in headers,
            "has_x_token": "x-token" in headers,
        },
        "body_keys": list(body.keys()) if isinstance(body, dict) else [],
        "body_auth_fields": {
            "password": keyinfo(body, "password"),
            "apiKey": keyinfo(body, "apiKey"),
            "token": keyinfo(body, "token"),
            "params.password": keyinfo(params or {}, "password") if isinstance(params, dict) else None,
            "params.apiKey": keyinfo(params or {}, "apiKey") if isinstance(params, dict) else None,
            "params.token": keyinfo(params or {}, "token") if isinstance(params, dict) else None,
        },
    }
