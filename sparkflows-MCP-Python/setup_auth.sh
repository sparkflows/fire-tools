#!/usr/bin/env bash
set -euo pipefail

# Customize if you want
export MCP_JWT_ISS="${MCP_JWT_ISS:-sparkflows-mcp}"
export MCP_JWT_AUD="${MCP_JWT_AUD:-mcp-clients}"
export MCP_CLIENT_ID="${MCP_CLIENT_ID:-my-client}"
export MCP_CLIENT_SECRET="${MCP_CLIENT_SECRET:-super-secret}"

# Generate a long random secret (base64)
if command -v openssl >/dev/null 2>&1; then
  export MCP_JWT_SECRET="$(openssl rand -base64 64)"
else
  export MCP_JWT_SECRET="$(python3 - <<'PY'
import secrets, base64; print(base64.b64encode(secrets.token_bytes(64)).decode())
PY
)"
fi

echo "Auth env set (secrets hidden). Start server in THIS shell:"
echo "  uvicorn app:app --host 0.0.0.0 --port 8090 --reload"
