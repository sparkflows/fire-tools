"""
controllers/mcp_jsonrpc.py

FastAPI controller that exposes:
  1) A simple JSON-RPC-like endpoint at POST "/"
  2) MCP-style HTTP transport:
       - GET  /sse           -> opens an SSE stream; returns a session id in headers
       - POST /mcp/message   -> accepts JSON-RPC requests, routes replies via that SSE session

This mirrors the Java Spring AI MCP WebMVC transport pattern while preserving the
easy curl-able "/" endpoint for direct tests.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from typing import Any, Dict, List, Tuple
import asyncio
import json
import time
import uuid

from services.mysql_mcp_service import MySqlMcpService

# Setup
router = APIRouter()
svc = MySqlMcpService()

# Session registry for SSE: sid -> asyncio.Queue (server -> client messages)
_sessions: Dict[str, asyncio.Queue] = {}


# Helpers

def _tool_entry(
    name: str,
    description: str,
    properties: Dict[str, Any],
    required: List[str],
) -> Dict[str, Any]:
    """Build a tool descriptor (mirrors the Java controller's tools/list shape)."""
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
    """Wrap a tool's successful payload into MCP 'content' envelope."""
    return {"content": [{"type": "text", "text": text}], "isError": False}


def _err_content(msg: str) -> Dict[str, Any]:
    """Wrap an error message into MCP 'content' envelope."""
    return {"content": [{"type": "text", "text": f"Error: {msg}"}], "isError": True}


def _tools_list() -> Dict[str, Any]:
    """Return the tools metadata (same as Java)."""
    tools: List[Dict[str, Any]] = []

    # Resource-backed tools
    tools.append(_tool_entry(
        "createWorkflow",
        "Create workflow - returns the workflow JSON",
        {},
        []
    ))
    tools.append(_tool_entry(
        "LegoblockXMLParser",
        "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)",
        {},
        []
    ))
    tools.append(_tool_entry(
        "LegoblockXMLMapping",
        "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)",
        {},
        []
    ))
    tools.append(_tool_entry(
        "createPipelineNode",
        "Create pipeline node - returns the pipeline node JSON",
        {},
        []
    ))
    tools.append(_tool_entry(
        "createWorkflowNode",
        "Create workflow node - returns the workflow node JSON",
        {},
        []
    ))

    # Constructed tools
    tools.append(_tool_entry(
        "CreateExtractionLegoBlock",
        "Create an extraction lego block by combining 2 strings",
        {
            "first_string": {"type": "string", "description": "First string"},
            "second_string": {"type": "string", "description": "Second string"},
        },
        ["first_string", "second_string"]
    ))

    tools.append(_tool_entry(
        "logoblockXMl",
        "Create a small XML block descriptor",
        {
            "ClusterId": {"type": "string", "description": "Cluster ID"},
            "StepName": {"type": "string", "description": "Step name"},
            "deploy-mode": {"type": "string", "description": "Deployment mode (cluster/client)"},
        },
        ["ClusterId", "StepName", "deploy-mode"]
    ))

    tools.append(_tool_entry(
        "ReadCSV",
        "Read CSV file from the specified path",
        {"path": {"type": "string", "description": "Path to the CSV file to read"}},
        ["path"]
    ))

    return {"tools": tools}


def _initialize() -> Dict[str, Any]:
    """Return MCP initialize payload (similar to Java)."""
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
    """
    Dispatch a tool call and return (ok, payload_string).
    The payload_string is what we place into 'content[0].text' to mirror Java behavior.
    """
    try:
        # Resource-backed tools
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

        # Constructed tools
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

        # Unknown tool
        return False, f"Tool not found: {name}"

    except KeyError as e:
        return False, f"Missing required argument: {e}"
    except Exception as e:
        return False, str(e)



# JSON-RPC (simple) endpoint at "/"

@router.post("/")
async def json_rpc_root(req: Request):
    """
    Synchronous JSON-RPC-ish handler (no SSE). Useful for curl tests and parity with earlier Python demo.
    """
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


# ---------------------------------------------------------------------------
# MCP HTTP transport: /sse and /mcp/message
# ---------------------------------------------------------------------------

async def _heartbeat_writer(q: asyncio.Queue):
    """Optional heartbeat events to keep SSE alive."""
    while True:
        await asyncio.sleep(15)
        await q.put({"event": "heartbeat", "data": {"ts": time.time()}})


@router.get("/sse")
async def sse():
    sid = str(uuid.uuid4())
    q: asyncio.Queue = asyncio.Queue()
    _sessions[sid] = q

    # push first event so clients can read SID from the stream
    q.put_nowait({"event": "session", "data": {"sid": sid}})

    # heartbeat to keep connection alive
    asyncio.create_task(_heartbeat_writer(q))

    async def event_gen():
        try:
            while True:
                payload = await q.get()
                event = payload.get("event", "message")
                data = json.dumps(payload.get("data", {}), ensure_ascii=False)
                yield {"event": event, "data": data}
        except asyncio.CancelledError:
            pass
        finally:
            _sessions.pop(sid, None)

    # set header on the EventSourceResponse object
    resp = EventSourceResponse(event_gen())
    resp.headers["Mcp-Session-Id"] = sid
    return resp



@router.post("/mcp/message")
async def mcp_message(req: Request):
    """
    Receive a JSON-RPC message from client -> server.
    Route the full JSON-RPC response to the associated SSE session (server -> client).
    Return a small ACK immediately (typical MCP HTTP behavior).
    """
    body = await req.json()
    sid = req.headers.get("Mcp-Session-Id")
    if not sid or sid not in _sessions:
        return JSONResponse(status_code=400, content={"error": "Missing or invalid Mcp-Session-Id"})

    method = body.get("method")
    _id = body.get("id")
    params = body.get("params", {})

    try:
        # Reuse existing handlers
        if method == "tools/list":
            result = _tools_list()
        elif method == "initialize":
            result = _initialize()
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            ok, payload = _call_tool(name, arguments)
            result = _ok_content(payload) if ok else _err_content(payload)
        else:
            # JSON-RPC error over SSE
            err = {"id": _id, "jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}}
            await _sessions[sid].put({"event": "rpc", "data": err})
            return {"ok": False}

        # Push JSON-RPC response over SSE
        await _sessions[sid].put({
            "event": "rpc",
            "data": {"id": _id, "jsonrpc": "2.0", "result": result}
        })

        # Immediate ACK to the POST
        return {"ok": True}

    except Exception as e:
        err = {"id": _id, "jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}
        await _sessions[sid].put({"event": "rpc", "data": err})
        return {"ok": False}
