# mysql_mcp_service.py
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

import json
import uuid

from fastapi import HTTPException

# Base dir of this file; resources/ lives in the same folder
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"


# ---------- Helpers ----------

def load_resource(relative_path: str) -> str:
    path = RESOURCES_DIR / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Resource not found: {relative_path} (expected at {path})",
        )


def wrap_tool_result_text(text: str) -> Dict[str, Any]:
    return {
        "content": [{"type": "text", "text": text}],
        "isError": False,
    }


def wrap_tool_error_text(message: str) -> Dict[str, Any]:
    return {
        "content": [{"type": "text", "text": f"Error: {message}"}],
        "isError": True,
    }


def get_initialize_response() -> Dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {
                "listChanged": True,
            }
        },
        "serverInfo": {
            "name": "MCP Shopping List Server",
            "version": "1.0.0",
        },
    }


def create_tool(
    name: str,
    description: str,
    properties: Dict[str, Any],
    required: List[str],
) -> Dict[str, Any]:
    input_schema = {
        "type": "object",
        "properties": properties,
        "required": required,
    }

    output_schema = {
        "type": "object",
        "properties": {
            "content": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "text": {"type": "string"},
                    },
                },
            },
            "isError": {"type": "boolean"},
        },
        "required": ["content", "isError"],
    }

    return {
        "name": name,
        "description": description,
        "input_schema": input_schema,
        "output_schema": output_schema,
        "next_steps": {},
    }


# ---------- Tool definitions ----------

def get_tools_list() -> Dict[str, Any]:
    tools: List[Dict[str, Any]] = []

    tools.append(
        create_tool(
            "createWorkflow",
            "Create workflow - returns the workflow JSON",
            {},
            [],
        )
    )
    tools.append(
        create_tool(
            "LegoblockXMLParser",
            "Lego Block: Execute Generic XML Parser (a wrapper around Spark XML)",
            {},
            [],
        )
    )
    tools.append(
        create_tool(
            "LegoblockXMLMapping",
            "Lego Block: Execute Mapping Language Pipeline (a wrapper around Mapping Language Engine)",
            {},
            [],
        )
    )
    tools.append(
        create_tool(
            "createPipelineNode",
            "Create pipeline node - returns the pipeline node JSON",
            {},
            [],
        )
    )
    tools.append(
        create_tool(
            "createWorkflowNode",
            "Create workflow node - returns the workflow node JSON",
            {},
            [],
        )
    )

    # Dynamic tools
    tools.append(
        create_tool(
            "CreateExtractionLegoBlock",
            "Create an Extraction Lego Block with specified configuration",
            {
                "first_string": {
                    "type": "string",
                    "description": "Source input string",
                },
                "second_string": {
                    "type": "string",
                    "description": "Target output string",
                },
            },
            ["first_string", "second_string"],
        )
    )

    # Logo Block XML Parser Tool
    tools.append(
        create_tool(
            "logoblockXMl",
            "Parse XML for Logo Block with cluster and deployment configuration",
            {
                "ClusterId": {
                    "type": "string",
                    "description": "Cluster identifier for the logo block",
                },
                "StepName": {
                    "type": "string",
                    "description": "Name of the execution step",
                },
                "deploy-mode": {
                    "type": "string",
                    "description": "Deployment mode (e.g., cluster, client)",
                },
            },
            ["ClusterId", "StepName", "deploy-mode"],
        )
    )

    tools.append(
        create_tool(
            "ReadCSV",
            "Read CSV file from the specified path",
            {
                "path": {
                    "type": "string",
                    "description": "Path to the CSV file to read",
                }
            },
            ["path"],
        )
    )

    return {"tools": tools}


# ---------- Tool implementations ----------

def create_workflow() -> str:
    return load_resource("workflow/Read-And-Display-Data.json")


def legoblock_xml_parser() -> str:
    return load_resource("pipeline/xmlparser.json")


def legoblock_xml_mapping() -> str:
    return load_resource("pipeline/xmlMapping.json")


def create_pipeline_node() -> str:
    return load_resource("pipeline_node/branchPythonOperator.json")


def create_workflow_node() -> str:
    return load_resource("workflow_node/csv.json")


def create_extraction_lego_block(first_string: str, second_string: str) -> str:
    if not first_string or not first_string.strip() or not second_string or not second_string.strip():
        raise ValueError("Both first_string and second_string are required")

    block_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().isoformat()

    input_processing: Dict[str, Any] = {
        "source": first_string,
        "validation": True,
        "encoding": "utf-8",
    }

    output_processing: Dict[str, Any] = {
        "target": second_string,
        "format": "json",
        "compression": "none",
    }

    extraction_rules = [
        {"type": "field_mapping", "rule": "map_source_to_target"},
        {"type": "filter", "rule": "exclude_empty_rows"},
    ]

    settings = {
        "inputProcessing": input_processing,
        "outputProcessing": output_processing,
        "extractionRules": extraction_rules,
    }

    configuration = {
        "blockId": block_id,
        "extractionType": "data_extraction",
        "sourceInput": first_string,
        "targetOutput": second_string,
        "timestamp": timestamp,
        "settings": settings,
    }

    location = {
        "x": 100,
        "y": 150,
        "width": 200,
        "height": 100,
        "zIndex": 1,
        "gridAlign": True,
    }

    parameters = [
        {
            "configuration": json.dumps(configuration),
            "type": "string",
            "description": "Configuration Parameter",
        },
        {
            "location": json.dumps(location),
            "type": "string",
            "description": "Location Parameter",
        },
    ]

    next_steps = [
        {
            "action": "create_node",
            "node_name": "ExtractionLegoBlock",
            "parameters": parameters,
            "required": ["message", "next_steps"],
        }
    ]

    response = {
        "tool_name": "CreateExtractionLegoBlock",
        "status": "success",
        "result": {"message": "Create an Extraction Lego Block"},
        "next_steps": next_steps,
    }

    return json.dumps(response)

def create_logoblock_xml(cluster_id: str, step_name: str, deploy_mode: str) -> str:
    """
    Python createLogoblockXMl(String clusterId, String stepName, String deployMode).
    Builds XML parser config and next_steps for the Logo Block.
    """
    if not cluster_id or not cluster_id.strip() or \
       not step_name or not step_name.strip() or \
       not deploy_mode or not deploy_mode.strip():
        raise ValueError("ClusterId, StepName, and deploy-mode are all required")

    block_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().isoformat()

    # Cluster configuration
    cluster_config = {
        "clusterId": cluster_id,
        "region": "us-east-1",
        "instanceType": "m5.xlarge",
        "autoScaling": True,
    }

    # Step configuration
    step_config = {
        "stepName": step_name,
        "actionOnFailure": "CONTINUE",
        "hadoopJarStep": {
            "jar": "command-runner.jar",
            "args": ["spark-submit", "--deploy-mode", deploy_mode],
        },
    }

    # Deployment configuration
    deployment_config = {
        "deployMode": deploy_mode,
        "driverMemory": "2g",
        "executorMemory": "4g",
        "executorCores": 2,
        "numExecutors": 3,
    }

    # Processing rules
    processing_rules = [
        {"type": "xml_validation", "enabled": True},
        {"type": "schema_validation", "enabled": True},
        {"type": "transformation", "enabled": True},
    ]

    settings = {
        "clusterConfig": cluster_config,
        "stepConfig": step_config,
        "deploymentConfig": deployment_config,
        "processingRules": processing_rules,
    }

    xml_parser_config = {
        "blockId": block_id,
        "parserType": "xml_logoblock_parser",
        "clusterId": cluster_id,
        "stepName": step_name,
        "deployMode": deploy_mode,
        "timestamp": timestamp,
        "settings": settings,
    }

    position = {
        "x": 150,
        "y": 200,
        "width": 250,
        "height": 120,
        "zIndex": 1,
        "gridAlign": True,
    }

    parameters = [
        {
            "ClusterId": cluster_id,
            "type": "string",
            "description": "Cluster identifier for the logo block",
        },
        {
            "StepName": step_name,
            "type": "string",
            "description": "Name of the execution step",
        },
        {
            "deployMode": deploy_mode,
            "type": "string",
            "description": "Deployment mode (e.g., cluster, client)",
        },
        {
            "xmlParserConfig": json.dumps(xml_parser_config),
            "type": "string",
            "description": "XML Parser Configuration Parameter",
        },
        {
            "position": json.dumps(position),
            "type": "string",
            "description": "Position Parameter",
        },
    ]

    next_steps = [
        {
            "action": "create_node",
            "node_name": "XMLMapping",
            "parameters": parameters,
            "required": ["message", "next_steps"],
        }
    ]

    response = {
        "tool_name": "logoblockXMl",
        "status": "success",
        "result": {"message": "Parse XML for Logo Block with cluster configuration"},
        "next_steps": next_steps,
    }

    return json.dumps(response)


def create_read_csv(path: str) -> str:
    if not path or not path.strip():
        raise ValueError("path is required")

    block_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().isoformat()

    csv_config: Dict[str, Any] = {
        "blockId": block_id,
        "path": path,
        "delimiter": ",",
        "header": True,
        "encoding": "utf-8",
        "timestamp": timestamp,
    }

    position: Dict[str, Any] = {
        "x": 150,
        "y": 200,
        "width": 250,
        "height": 120,
        "zIndex": 1,
        "gridAlign": True,
    }

    parameters = [
        {
            "path": path,
            "type": "string",
            "description": "Path to the CSV file",
        },
        {
            "csvConfig": json.dumps(csv_config),
            "type": "string",
            "description": "CSV Configuration Parameter",
        },
        {
            "position": json.dumps(position),
            "type": "string",
            "description": "Position Parameter",
        },
    ]

    next_steps = [
        {
            "action": "create_node",
            "node_name": "Read CSV",
            "parameters": parameters,
            "required": ["message", "next_steps"],
        }
    ]

    response = {
        "tool_name": "ReadCSV",
        "status": "success",
        "result": {"message": "Read CSV file from path"},
        "next_steps": next_steps,
    }

    return json.dumps(response)


# ---------- Dispatcher ----------

def handle_tool_call(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        tool_name = params["name"]
        arguments = params.get("arguments") or {}
    except KeyError:
        raise ValueError("Missing 'name' or 'arguments' in params")

    try:
        if tool_name == "createWorkflow":
            result_str = create_workflow()
        elif tool_name == "LegoblockXMLParser":
            result_str = legoblock_xml_parser()
        elif tool_name == "LegoblockXMLMapping":
            result_str = legoblock_xml_mapping()
        elif tool_name == "createPipelineNode":
            result_str = create_pipeline_node()
        elif tool_name == "createWorkflowNode":
            result_str = create_workflow_node()

        elif tool_name == "CreateExtractionLegoBlock":
            first = arguments.get("first_string")
            second = arguments.get("second_string")
            result_str = create_extraction_lego_block(first, second)

        elif tool_name == "logoblockXMl":
            cluster_id = arguments.get("ClusterId")
            step_name = arguments.get("StepName")
            deploy_mode = arguments.get("deploy-mode")
            result_str = create_logoblock_xml(cluster_id, step_name, deploy_mode)

        elif tool_name == "ReadCSV":
            path = arguments.get("path")
            result_str = create_read_csv(path)

        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        return wrap_tool_result_text(result_str)

    except Exception as e:
        return wrap_tool_error_text(str(e))
