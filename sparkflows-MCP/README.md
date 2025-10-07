# Sparkflows MCP Workflow Server

This is a Spring Boot MCP (Model Context Protocol) server that provides workflow and pipeline management tools for Sparkflows.

## Project Overview

The server exposes 8 MCP tools for creating and managing workflows, pipelines, and data processing blocks:

- **createWorkflow** - Create workflow and returns workflow JSON
- **LegoblockXMLParser** - Execute Generic XML Parser (wrapper around Spark XML)
- **LegoblockXMLMapping** - Execute Mapping Language Pipeline (wrapper around Mapping Language Engine)
- **createPipelineNode** - Create pipeline node and returns pipeline node JSON
- **createWorkflowNode** - Create workflow node and returns workflow node JSON
- **CreateExtractionLegoBlock** - Create an Extraction Lego Block with specified configuration
- **logoblockXMl** - Parse XML for Logo Block with cluster and deployment configuration
- **ReadCSV** - Read CSV file from the specified path

## Project Structure

```
src/
├── main/
│   ├── java/com/sparkflows/
│   │   ├── SparkflowsMcpApplication.java    # Main Spring Boot application
│   │   ├── McpJsonRpcController.java        # JSON-RPC MCP endpoint handler
│   │   └── MySqlMcpService.java             # Service containing MCP tool implementations
│   └── resources/
│       ├── application.properties           # Application configuration
│       ├── pipeline/                        # Pipeline configuration JSONs
│       ├── pipeline_node/                   # Pipeline node configuration JSONs
│       ├── workflow/                        # Workflow configuration JSONs
│       └── workflow_node/                   # Workflow node configuration JSONs
```

## Prerequisites

- Java 17 or higher
- Maven 3.6+

## Building the Project

Build the project using Maven:

```bash
mvn clean install
```

## Running the Server

### Option 1: Using Maven
```bash
mvn spring-boot:run
```

### Option 2: Using the JAR file
```bash
java -jar target/mcp-workflow-server-0.0.1-SNAPSHOT.jar
```

The server will start on port **8090** by default.

## Configuration

Key configurations in `application.properties`:

- **Server Port**: `8090`
- **Application Name**: `mcp-workflow-server`
- **CORS**: Enabled for ChatGPT and OpenAI domains

## API Endpoints

### MCP JSON-RPC Endpoint
**POST** `/mcp/rpc`

The server implements the MCP protocol via JSON-RPC 2.0 over HTTP.

#### Supported Methods:
- `initialize` - Initialize MCP connection
- `tools/list` - List all available tools
- `tools/call` - Execute a specific tool

#### Example Request:
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/list"
}
```

## Tool Usage Examples

### CreateExtractionLegoBlock
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "CreateExtractionLegoBlock",
    "arguments": {
      "first_string": "input_source",
      "second_string": "output_target"
    }
  }
}
```

### ReadCSV
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "ReadCSV",
    "arguments": {
      "path": "/data/input.csv"
    }
  }
}
```

## Technologies Used

- **Spring Boot 3.5.0** - Application framework
- **Spring AI 1.0.0** - MCP server implementation
- **Jackson** - JSON processing
- **Java 17** - Programming language


