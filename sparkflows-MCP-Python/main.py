# # main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Any, Dict, List, Optional, Union
# from pathlib import Path
# from datetime import datetime
# import json
# import uuid

# app = FastAPI()

# # Base directory of this file
# BASE_DIR = Path(__file__).resolve().parent
# # Mirror the Java classpath resources:
# #   workflow/Read-And-Display-Data.json
# #   workflow_node/csv.json
# #   pipeline/xmlparser.json
# #   pipeline/xmlMapping.json
# #   pipeline_node/branchPythonOperator.json
# RESOURCES_DIR = BASE_DIR / "resources"


# class JSONRPCRequest(BaseModel):
#     jsonrpc: Union[str, int, None] = "2.0"
#     id: Union[str, int, None] = None
#     method: str
#     params: Optional[Dict[str, Any]] = None


# def load_resource(relative_path: str) -> str:
#     """
#     Equivalent of Java's ClassPathResource("...").readAllBytes().
#     Looks for resources/<relative_path>.
#     """
#     path = RESOURCES_DIR / relative_path
#     try:
#         return path.read_text(encoding="utf-8")
#     except FileNotFoundError:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Resource not found: {relative_path} (expected at {path})",
#         )


# def wrap_tool_result_text(text: str) -> Dict[str, Any]:
#     """
#     Java handleToolCall returns:
#       { "content": [ { "type": "text", "text": resultString } ], "isError": false }
#     where resultString is often a JSON string.
#     """
#     return {
#         "content": [{"type": "text", "text": text}],
#         "isError": False,
#     }


# def wrap_tool_error_text(message: str) -> Dict[str, Any]:
#     return {
#         "content": [{"type": "text", "text": f"Error: {message}"}],
#         "isError": True,
#     }


# def get_initialize_response() -> Dict[str, Any]:
#     # Mirrors Java getInitializeResponse()
#     return {
#         "protocolVersion": "2024-11-05",
#         "capabilities": {
#             "tools": {
#                 "listChanged": True,
#             }
#         },
#         "serverInfo": {
#             "name": "MCP Shopping List Server",  # same as Java
#             "version": "1.0.0",
#         },
#     }


# def create_tool(
#     name: str,
#     description: str,
#     properties: Dict[str, Any],
#     required: List[str],
# ) -> Dict[str, Any]:
#     """
#     Mirrors Java createTool() helper:
#       - input_schema is object with properties + required
#       - output_schema describes { content: [...], isError: boolean }
#     """
#     input_schema = {
#         "type": "object",
#         "properties": properties,
#         "required": required,
#     }

#     output_schema = {
#         "type": "object",
#         "properties": {
#             "content": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "type": {"type": "string"},
#                         "text": {"type": "string"},
#                     },
#                 },
#             },
#             "isError": {"type": "boolean"},
#         },
#         "required": ["content", "isError"],
#     }

#     return {
#         "name": name,
#         "description": description,
#         "input_schema": input_schema,
#         "output_schema": output_schema,
#         # Java also tacks on an empty "next_steps" map; we can omit or include.
#         "next_steps": {},
#     }


# def get_tools_list() -> Dict[str, Any]:
#     """
#     Mirrors Java getToolsList() as closely as we need right now.
#     """
#     tools: List[Dict[str, Any]] = []

#     # Workflow tools that just return JSON from resources
#     tools.append(
#         create_tool(
#             "createWorkflow",
#             "Create workflow - returns the workflow JSON",
#             {},
#             [],
#         )
#     )
#     tools.append(
#         create_tool(
#             "LegoblockXMLParser",
#             "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)",
#             {},
#             [],
#         )
#     )
#     tools.append(
#         create_tool(
#             "LegoblockXMLMapping",
#             "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)",
#             {},
#             [],
#         )
#     )
#     tools.append(
#         create_tool(
#             "createPipelineNode",
#             "Create pipeline node - returns the pipeline node JSON",
#             {},
#             [],
#         )
#     )
#     tools.append(
#         create_tool(
#             "createWorkflowNode",
#             "Create workflow node - returns the workflow node JSON",
#             {},
#             [],
#         )
#     )

#     # Extraction Lego Block tool (your example with first_string/second_string)
#     tools.append(
#         create_tool(
#             "CreateExtractionLegoBlock",
#             "Create an Extraction Lego Block with specified configuration",
#             {
#                 "first_string": {
#                     "type": "string",
#                     "description": "Source input string",
#                 },
#                 "second_string": {
#                     "type": "string",
#                     "description": "Target output string",
#                 },
#             },
#             ["first_string", "second_string"],
#         )
#     )

#     # Read CSV tool (takes a path, returns next_steps to create Read CSV node)
#     tools.append(
#         create_tool(
#             "ReadCSV",
#             "Read CSV file from the specified path",
#             {
#                 "path": {
#                     "type": "string",
#                     "description": "Path to the CSV file to read",
#                 }
#             },
#             ["path"],
#         )
#     )

#     return {"tools": tools}


# def create_extraction_lego_block(first_string: str, second_string: str) -> str:
#     """
#     Python port of Java createExtractionLegoBlock().
#     Returns a JSON string that has:
#       { "tool_name": "...", "status": "...", "result": {...}, "next_steps": [...] }
#     """
#     if not first_string or not first_string.strip() or not second_string or not second_string.strip():
#         raise ValueError("Both first_string and second_string are required")

#     block_id = uuid.uuid4().hex[:8]
#     timestamp = datetime.now().isoformat()

#     # These structures are simplified but follow the same spirit as the Java version.
#     input_processing = {
#         "source": first_string,
#         "validation": True,
#         "encoding": "utf-8",
#     }

#     output_processing = {
#         "target": second_string,
#         "format": "json",
#         "compression": "none",
#     }

#     extraction_rules = [
#         {"type": "field_mapping", "rule": "map_source_to_target"},
#         {"type": "filter", "rule": "exclude_empty_rows"},
#     ]

#     settings = {
#         "inputProcessing": input_processing,
#         "outputProcessing": output_processing,
#         "extractionRules": extraction_rules,
#     }

#     configuration = {
#         "blockId": block_id,
#         "extractionType": "data_extraction",
#         "sourceInput": first_string,
#         "targetOutput": second_string,
#         "timestamp": timestamp,
#         "settings": settings,
#     }

#     location = {
#         "x": 100,
#         "y": 150,
#         "width": 200,
#         "height": 100,
#         "zIndex": 1,
#         "gridAlign": True,
#     }

#     parameters = [
#         {
#             "configuration": json.dumps(configuration),
#             "type": "string",
#             "description": "Configuration Parameter",
#         },
#         {
#             "location": json.dumps(location),
#             "type": "string",
#             "description": "Location Parameter",
#         },
#     ]

#     next_steps = [
#         {
#             "action": "create_node",
#             "node_name": "ExtractionLegoBlock",
#             "parameters": parameters,
#             "required": ["message", "next_steps"],
#         }
#     ]

#     response = {
#         "tool_name": "CreateExtractionLegoBlock",
#         "status": "success",
#         "result": {"message": "Create an Extraction Lego Block"},
#         "next_steps": next_steps,
#     }

#     return json.dumps(response)


# def create_read_csv(path: str) -> str:
#     """
#     Python port of Java createReadCSV(String path).
#     This is the one you care about for:

#       "Create read csv node with path S3://testdir/test.csv"
#     """
#     if not path or not path.strip():
#         raise ValueError("path is required")

#     block_id = uuid.uuid4().hex[:8]
#     timestamp = datetime.now().isoformat()

#     csv_config = {
#         "blockId": block_id,
#         "path": path,
#         "delimiter": ",",
#         "header": True,
#         "encoding": "utf-8",
#         "timestamp": timestamp,
#     }

#     position = {
#         "x": 150,
#         "y": 200,
#         "width": 250,
#         "height": 120,
#         "zIndex": 1,
#         "gridAlign": True,
#     }

#     parameters = [
#         {
#             "path": path,
#             "type": "string",
#             "description": "Path to the CSV file",
#         },
#         {
#             "csvConfig": json.dumps(csv_config),
#             "type": "string",
#             "description": "CSV Configuration Parameter",
#         },
#         {
#             "position": json.dumps(position),
#             "type": "string",
#             "description": "Position Parameter",
#         },
#     ]

#     next_steps = [
#         {
#             "action": "create_node",
#             "node_name": "Read CSV",
#             "parameters": parameters,
#             "required": ["message", "next_steps"],
#         }
#     ]

#     response = {
#         "tool_name": "ReadCSV",
#         "status": "success",
#         "result": {"message": "Read CSV file from path"},
#         "next_steps": next_steps,
#     }

#     return json.dumps(response)


# def handle_tool_call(params: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Equivalent of Java handleToolCall(JsonNode params).
#     """
#     try:
#         tool_name = params["name"]
#         arguments = params.get("arguments") or {}
#     except KeyError:
#         raise ValueError("Missing 'name' or 'arguments' in params")

#     try:
#         # ---- Tools backed by resource JSONs (MySqlMcpService) ----
#         if tool_name == "createWorkflow":
#             result_str = load_resource("workflow/Read-And-Display-Data.json")
#         elif tool_name == "LegoblockXMLParser":
#             result_str = load_resource("pipeline/xmlparser.json")
#         elif tool_name == "LegoblockXMLMapping":
#             result_str = load_resource("pipeline/xmlMapping.json")
#         elif tool_name == "createPipelineNode":
#             result_str = load_resource("pipeline_node/branchPythonOperator.json")
#         elif tool_name == "createWorkflowNode":
#             result_str = load_resource("workflow_node/csv.json")

#         # ---- Dynamic tools ----
#         elif tool_name == "CreateExtractionLegoBlock":
#             first = arguments.get("first_string")
#             second = arguments.get("second_string")
#             result_str = create_extraction_lego_block(first, second)

#         elif tool_name == "ReadCSV":
#             path = arguments.get("path")
#             result_str = create_read_csv(path)

#         else:
#             raise ValueError(f"Unknown tool: {tool_name}")

#         return wrap_tool_result_text(result_str)

#     except Exception as e:
#         # Match Java pattern: error with isError=true
#         return wrap_tool_error_text(str(e))


# @app.post("/rpc")
# async def rpc_handler(request: JSONRPCRequest) -> Dict[str, Any]:
#     """
#     Port of McpJsonRpcController.handleJsonRpc().
#     """
#     response: Dict[str, Any] = {
#         "jsonrpc": "2.0",
#         "id": request.id or "1",
#     }

#     try:
#         method = request.method

#         if method == "tools/list":
#             response["result"] = get_tools_list()

#         elif method == "tools/call":
#             if request.params is None:
#                 raise ValueError("Missing params for tools/call")
#             response["result"] = handle_tool_call(request.params)

#         elif method == "initialize":
#             response["result"] = get_initialize_response()

#         else:
#             response["error"] = {
#                 "code": -32601,
#                 "message": f"Method not found: {method}",
#             }

#     except Exception as e:
#         response["error"] = {
#             "code": -32603,
#             "message": f"Internal error: {e}",
#         }

#     return response

# main.py
from fastapi import FastAPI
from mcp_json_rpc_controller import router as rpc_router

app = FastAPI()

# Register the JSON-RPC controller (like Spring's @RestController)
app.include_router(rpc_router)
