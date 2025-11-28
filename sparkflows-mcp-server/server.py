from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

# Import your existing logic from the old code
from mysql_mcp_service import (
    create_workflow,
    legoblock_xml_parser,
    legoblock_xml_mapping,
    create_pipeline_node,
    create_workflow_node,
    create_extraction_lego_block,
    create_logoblock_xml,
    create_read_csv,
    wrap_tool_result_text,
    wrap_tool_error_text,
)

# ============================================================================
# MCP SERVER SETUP
# ============================================================================

# This creates a "normal" MCP server that can be used by MCP clients
# (Claude Desktop, VS Code, ChatGPT MCP, etc.).
mcp = FastMCP(
    name="sparkflows-mcp-server",
    stateless_http=True,   # HTTP transport, no server-side sessions
    json_response=True,    # JSON responses
)

# ============================================================================
# NEW TOOLS: parquet_schema + read_extraction_config
# ============================================================================

@mcp.tool()
def parquet_schema(path: str, limit: int = 5) -> Dict[str, Any]:
    """
    Inspect a Parquet file and return schema + sample rows.

    Args:
        path: Path to a Parquet file (local or accessible from the server).
        limit: Max number of sample rows to include from the first row group.

    Returns:
        {
          "path": "<path>",
          "num_row_groups": <int>,
          "fields": [
            {"name": "<col>", "type": "<arrow-type>", "nullable": <bool>},
            ...
          ],
          "sample_rows": [
            {"col1": ..., "col2": ...},
            ...
          ]
        }
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
    path: str = "extraction_config_template.json",
) -> Dict[str, Any]:
    """
    Read an extraction config template from a local file.

    Args:
        path: Path to the config file. Defaults to
              'extraction_config_template.json' in the project root.

    Returns:
        {
          "path": "<path>",
          "config": <parsed-json-or-None>,
          "raw": "<raw-file-contents>"
        }
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Extraction config not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to parse as JSON; if that fails, just return raw text.
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = None

    return {
        "path": path,
        "config": parsed,
        "raw": content,
    }

# ============================================================================
# OLD CUSTOM TOOLS (wrapped as MCP tools)
# These all reuse your existing implementations from mysql_mcp_service.py.
# We preserve the original tool names for compatibility.
# ============================================================================

@mcp.tool()
def createWorkflow() -> Dict[str, Any]:
    """
    Tool: createWorkflow
    Create workflow - returns the workflow JSON.
    """
    try:
        result_str = create_workflow()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def LegoblockXMLParser() -> Dict[str, Any]:
    """
    Tool: LegoblockXMLParser
    Lego Block: Execute Generic XML Parser (wrapper around Spark XML).
    """
    try:
        result_str = legoblock_xml_parser()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def LegoblockXMLMapping() -> Dict[str, Any]:
    """
    Tool: LegoblockXMLMapping
    Lego Block: Execute Mapping Language Pipeline (Mapping Language Engine).
    """
    try:
        result_str = legoblock_xml_mapping()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def createPipelineNode() -> Dict[str, Any]:
    """
    Tool: createPipelineNode
    Create pipeline node - returns the pipeline node JSON.
    """
    try:
        result_str = create_pipeline_node()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def createWorkflowNode() -> Dict[str, Any]:
    """
    Tool: createWorkflowNode
    Create workflow node - returns the workflow node JSON.
    """
    try:
        result_str = create_workflow_node()
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))


@mcp.tool()
def CreateExtractionLegoBlock(first_string: str, second_string: str) -> Dict[str, Any]:
    """
    Tool: CreateExtractionLegoBlock

    Build an 'Extraction Lego Block' JSON config based on two input strings.

    Args:
        first_string: Source string / input.
        second_string: Target string / output.
    """
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
    """
    Tool: logoblockXMl

    Parse XML for Logo Block with cluster and deployment configuration.

    Args:
        ClusterId: Cluster identifier for the logo block.
        StepName: Name of the execution step.
        deploy_mode: Deployment mode (e.g., 'cluster', 'client').
    """
    try:
        # Map parameters to your existing function signature
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
    """
    Tool: ReadCSV

    Create a CSV reader node configuration.

    Args:
        path: Path to the CSV file to read.
    """
    try:
        result_str = create_read_csv(path)
        return wrap_tool_result_text(result_str)
    except Exception as e:
        return wrap_tool_error_text(str(e))

# ============================================================================
# ENTRY POINT
# ============================================================================

def main() -> None:
    """
    Start the MCP server.

    Usage:
        uv run server.py
        or:
        python server.py

    This will start a Streamable HTTP MCP server on http://localhost:8000/mcp
    (default FastMCP HTTP settings).
    """
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
