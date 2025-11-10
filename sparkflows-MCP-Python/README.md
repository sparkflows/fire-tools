# Sparkflows-mcp-server (Python)

## Requirements
```
- Python 3.10+
- pip / venv
```

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

`requirements.txt`:
```
fastapi==0.115.0
uvicorn==0.30.6
python-multipart==0.0.9
```

---
## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 8090 --reload
```

Server starts on: `http://localhost:8090/`

---

## API (JSON-RPC-ish)

Single POST endpoint at `/`. Send a JSON-RPC-like body:

- **`initialize`**
- **`tools/list`**
- **`tools/call`**

Common envelope:

```json
{
  "id": "any-string",
  "jsonrpc": "2.0",
  "method": "<method-name>",
  "params": { ... }
}
```

### Methods

#### `initialize`

Request:

```json
{ "id":"1","jsonrpc":"2.0","method":"initialize","params":{} }
```

Response: basic server info + capabilities.

#### `tools/list`

Request:

```json
{ "id":"2","jsonrpc":"2.0","method":"tools/list","params":{} }
```

Response: array of tool descriptors with `input_schema` and `output_schema`.

#### `tools/call`

Request:

```json
{
  "id":"3","jsonrpc":"2.0","method":"tools/call",
  "params": {
    "name": "<ToolName>",
    "arguments": { /* tool-specific */ }
  }
}
```

Response:

```json
{
  "result": {
    "content": [{ "type": "text", "text": "<stringified JSON result>" }],
    "isError": false
  }
}
```

---

## Tools Exposed

**Resource-backed (return file contents as JSON string):**

- `createWorkflow` → `resources/workflow/Read-And-Display-Data.json`
- `LegoblockXMLParser` → `resources/pipeline/xmlparser.json`
- `LegoblockXMLMapping` → `resources/pipeline/xmlMapping.json`
- `createPipelineNode` → `resources/pipeline_node/xmlMapping.json`
- `createWorkflowNode` → `resources/workflow_node/csv.json`

**Constructed examples:**

- `CreateExtractionLegoBlock` (args: `first_string`, `second_string`)
- `logoblockXMl` (args: `ClusterId`, `StepName`, `deploy-mode`)
- `ReadCSV` (args: `path`)

---

## Quick Test (curl)

### List tools

```bash
curl -s http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -d '{"id":"1","jsonrpc":"2.0","method":"tools/list","params":{}}' | jq
```

### Call a resource-backed tool

```bash
curl -s http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -d '{"id":"2","jsonrpc":"2.0","method":"tools/call","params":{"name":"createWorkflow","arguments":{}}}' | jq
```

### Call ReadCSV

```bash
curl -s http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -d '{"id":"3","jsonrpc":"2.0","method":"tools/call","params":{"name":"ReadCSV","arguments":{"path":"/tmp/data.csv"}}}' | jq
```

### Call CreateExtractionLegoBlock

```bash
curl -s http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -d '{"id":"4","jsonrpc":"2.0","method":"tools/call","params":{"name":"CreateExtractionLegoBlock","arguments":{"first_string":"hello ","second_string":"world"}}}' | jq
```

---

## Notes

- CORS is permissive (mirrors the Java `application.properties` intent).
- If you want to change the port, adjust the `uvicorn` `--port` flag.
- All resource returns are **raw file contents** (kept identical to the Java behavior).