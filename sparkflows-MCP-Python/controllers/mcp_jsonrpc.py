from fastapi import APIRouter, Request
from typing import Any, Dict, List, Optional, Tuple

from services.mysql_mcp_service import MySqlMcpService

router = APIRouter()
svc = MySqlMcpService()

# ---- helpers ------------------------------------------------

def _tool_entry(
    name: str,
    description: str,
    properties: Dict[str, Any],
    required: List[str]
) -> Dict[str, Any]:
    # Mirrors the Java controller's tools/list shape
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

# ---- tools/list (same as Java) -------------------------------

def _tools_list() -> Dict[str, Any]:
    tools: List[Dict[str, Any]] = []

    # Workflow Tools (resource-backed)
    tools.append(_tool_entry("createWorkflow",
        "Create workflow - returns the workflow JSON",
        {}, []))
    tools.append(_tool_entry("LegoblockXMLParser",
        "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)",
        {}, []))
    tools.append(_tool_entry("LegoblockXMLMapping",
        "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)",
        {}, []))
    tools.append(_tool_entry("createPipelineNode",
        "Create pipeline node - returns the pipeline node JSON",
        {}, []))
    tools.append(_tool_entry("createWorkflowNode",
        "Create workflow node - returns the workflow node JSON",
        {}, []))

    # Extraction Lego Block (toy example)
    tools.append(_tool_entry("CreateExtractionLegoBlock",
        "Create an extraction lego block by combining 2 strings",
        {
            "first_string": {"type": "string", "description": "First string"},
            "second_string": {"type": "string", "description": "Second string"},
        },
        ["first_string", "second_string"]
    ))

    # Logo block XML (toy example to mirror Java)
    tools.append(_tool_entry("logoblockXMl",
        "Create a small XML block descriptor",
        {
            "ClusterId": {"type": "string", "description": "Cluster ID"},
            "StepName": {"type": "string", "description": "Step name"},
            "deploy-mode": {"type": "string", "description": "Deployment mode (cluster/client)"},
        },
        ["ClusterId", "StepName", "deploy-mode"]
    ))

    # Read CSV tool
    tools.append(_tool_entry("ReadCSV",
        "Read CSV file from the specified path",
        {
            "path": {"type": "string", "description": "Path to the CSV file to read"}
        },
        ["path"]
    ))

    return {"tools": tools}

# ---- initialize (same spirit as Java) ------------------------

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

# ---- tools/call dispatcher -----------------------------------

def _call_tool(name: str, arguments: Dict[str, Any]) -> Tuple[bool, str]:
    """Returns (ok, payload_string) to wrap into MCP content shape."""
    try:
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
            import json
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
            import json
            return True, json.dumps(result, ensure_ascii=False, indent=2)

        if name == "ReadCSV":
            a = arguments or {}
            path = a["path"]
            # Mirror Java: return a small, declarative JSON blob
            result = {
                "tool_name": "ReadCSV",
                "status": "success",
                "result": {"path": path, "format": "csv"},
                "next_steps": {},
            }
            import json
            return True, json.dumps(result, ensure_ascii=False, indent=2)

        # Unknown tool
        return False, f"Tool not found: {name}"

    except KeyError as e:
        return False, f"Missing required argument: {e}"
    except Exception as e:
        return False, str(e)

# ---- JSON-RPC endpoint ---------------------------------------

@router.post("/")
async def json_rpc_root(req: Request):
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
