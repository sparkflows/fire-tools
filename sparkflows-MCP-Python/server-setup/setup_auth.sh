#!/usr/bin/env bash
# Safe for sourcing: temporarily disable -u in the current shell
__had_u=0
case $- in *u*) __had_u=1; set +u;; esac
set -eo pipefail

export MCP_JWT_ISS="${MCP_JWT_ISS:-sparkflows-mcp}"
export MCP_JWT_AUD="${MCP_JWT_AUD:-mcp-clients}"
export MCP_CLIENT_ID="${MCP_CLIENT_ID:-my-client}"
export MCP_CLIENT_SECRET="${MCP_CLIENT_SECRET:-super-secret}"

# Generate signing key once per session
if command -v openssl >/dev/null 2>&1; then
  export MCP_JWT_SECRET="$(openssl rand -base64 64)"
else
  export MCP_JWT_SECRET="$(python3 - <<'PY'
import secrets, base64; print(base64.b64encode(secrets.token_bytes(64)).decode())
PY
)"
fi

echo "Auth env set in THIS shell (secrets hidden)."
echo "Next:"
echo "  1) Optionally: source server-setup/create_client.sh --subject \"dhruv\""
echo "  2) Start:      uvicorn app:app --host 0.0.0.0 --port 8090 --reload"

# restore -u if it was set
if [ $__had_u -eq 1 ]; then set -u; fi
unset __had_u
