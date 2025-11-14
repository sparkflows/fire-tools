# Sparkflows MCP (Python)

## Requirements

```bash
pip3 install fastapi uvicorn
```

## Launch Server

Note: Replace the MCP API KEY below in the terminal before launching the server.

```
export MCP_API_KEY=a7...
uvicorn main:app --host 0.0.0.0 --port 8090 --reload
```