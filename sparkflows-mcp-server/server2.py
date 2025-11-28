from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

import json
import os
import uuid

from mcp.server.fastmcp import FastMCP


# =============================================================================
# Paths (from old mysql_mcp_service.py)
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"


# =============================================================================
# Helper functions (from mysql_mcp_service.py)
# =============================================================================

def load_resource(relative_path: str) -> str:
    """
    Load a JSON template or other resource from the resources/ directory.
    """
    path = RESOURCES_DIR / relative_path
    if not path.exists():
        # FastMCP will surface this as a tool error
        raise FileNotFoundError(
            f"Resource not found: {relative_path} (expected at {path})"
        )
    return path.read_text(encoding="utf-8")


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


# ---------- Tool implementations (old mysql_mcp_service.py) ----------

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
    if (
        not first_string
        or not first_string.strip()
        or not second_string
        or not second_string.strip()
    ):
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
    Builds XML parser config and next_steps for the Logo Block.
    """
    if (
        not cluster_id
        or not cluster_id.strip()
        or not step_name
        or not step_name.strip()
        or not deploy_mode
        or not deploy_mode.strip()
    ):
        raise ValueError("ClusterId, StepName, and deploy-mode are all required")

    block_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().isoformat()

    cluster_config = {
        "clusterId": cluster_id,
        "region": "us-east-1",
        "instanceType": "m5.xlarge",
        "autoScaling": True,
    }

    step_config = {
        "stepName": step_name,
        "actionOnFailure": "CONTINUE",
        "hadoopJarStep": {
            "jar": "command-runner.jar",
            "args": ["spark-submit", "--deploy-mode", deploy_mode],
        },
    }

    deployment_config = {
        "deployMode": deploy_mode,
        "driverMemory": "2g",
        "executorMemory": "4g",
        "executorCores": 2,
        "numExecutors": 3,
    }

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
        "result": {
            "message": "Parse XML for Logo Block with cluster configuration"
        },
        "next_steps": next_steps,
    }

    return json.dumps(response)


def create_read_csv(path: str) -> str:
    if not path or not path.strip():
        raise ValueError("CSV path is required")

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


# =============================================================================
# MCP SERVER SETUP
# =============================================================================

mcp = FastMCP(
    name="sparkflows-mcp-server-2",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    port=8090,
)


# =============================================================================
# NEW TOOLS: parquet_schema + read_extraction_config
# =============================================================================

@mcp.tool()
def parquet_schema(path: str, limit: int = 5) -> Dict[str, Any]:
    """
    Inspect a Parquet file and return schema + sample rows.
    """
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError(
            "pyarrow is required for parquet_schema; "
            "please add 'pyarrow' to requirements.txt"
        ) from exc

    if not os.path.exists(path):
        raise FileNotFoundError(f"Parquet path not found: {path}")

    parquet_file = pq.ParquetFile(path)
    schema = parquet_file.schema_arrow

    fields: List[Dict[str, Any]] = []
    for i in range(len(schema)):
        field = schema[i]
        fields.append(
            {
                "name": field.name,
                "type": str(field.type),
                "nullable": field.nullable,
            }
        )

    sample_rows: List[Dict[str, Any]] = []
    if limit > 0 and parquet_file.num_row_groups > 0:
        table = parquet_file.read_row_groups([0])
        for row in table.to_pylist()[:limit]:
            sample_rows.append(row)

    return {
        "path": path,
        "num_row_groups": parquet_file.num_row_groups,
        "fields": fields,
        "sample_rows": sample_rows,
    }


@mcp.tool()
def read_extraction_config(
    path: str = "/data/extraction_config_template.json",
) -> Dict[str, Any]:
    """
    Read an extraction config template from a local file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Extraction config not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = None

    return {
        "path": path,
        "config": parsed,
        "raw": content,
    }


# =============================================================================
# OLD CUSTOM TOOLS EXPOSED AS MCP TOOLS
# =============================================================================

@mcp.tool()
def createWorkflow() -> Dict[str, Any]:
    try:
        result_str = create_workflow()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def LegoblockXMLParser() -> Dict[str, Any]:
    try:
        result_str = legoblock_xml_parser()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def LegoblockXMLMapping() -> Dict[str, Any]:
    try:
        result_str = legoblock_xml_mapping()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def createPipelineNode() -> Dict[str, Any]:
    try:
        result_str = create_pipeline_node()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def createWorkflowNode() -> Dict[str, Any]:
    try:
        result_str = create_workflow_node()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def CreateExtractionLegoBlock(first_string: str, second_string: str) -> Dict[str, Any]:
    try:
        result_str = create_extraction_lego_block(first_string, second_string)
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def logoblockXMl(
    ClusterId: str,
    StepName: str,
    deploy_mode: str,
) -> Dict[str, Any]:
    try:
        result_str = create_logoblock_xml(
            cluster_id=ClusterId,
            step_name=StepName,
            deploy_mode=deploy_mode,
        )
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def ReadCSV(path: str) -> Dict[str, Any]:
    try:
        result_str = create_read_csv(path)
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
