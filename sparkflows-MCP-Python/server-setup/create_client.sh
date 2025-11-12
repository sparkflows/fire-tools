#!/usr/bin/env bash
# Safe for sourcing: temporarily disable -u
__had_u=0
case $- in *u*) __had_u=1; set +u;; esac
set -eo pipefail

SUBJECT="${MCP_SUBJECT:-user}"
OUT="${OUT:-server-setup/client-credentials.json}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --subject) SUBJECT="${2:-}"; shift 2;;
    --subject=*) SUBJECT="${1#*=}"; shift;;
    --out) OUT="${2:-$OUT}"; shift 2;;
    --out=*) OUT="${1#*=}"; shift;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

# client_id / client_secret
if command -v uuidgen >/dev/null 2>&1; then
  CLIENT_ID=$(uuidgen | tr 'A-Z' 'a-z')
else
  CLIENT_ID=$(python3 - <<'PY'
import uuid; print(str(uuid.uuid4()))
PY
)
fi
if command -v openssl >/dev/null 2>&1; then
  CLIENT_SECRET=$(openssl rand -base64 48)
else
  CLIENT_SECRET=$(python3 - <<'PY'
import secrets, base64; print(base64.b64encode(secrets.token_bytes(48)).decode())
PY
)
fi

export MCP_CLIENT_ID="$CLIENT_ID"
export MCP_CLIENT_SECRET="$CLIENT_SECRET"

# write JSON safely
SUBJECT="$SUBJECT" MCP_CLIENT_ID="$MCP_CLIENT_ID" MCP_CLIENT_SECRET="$MCP_CLIENT_SECRET" \
python3 - <<'PY' > "$OUT"
import os, json
print(json.dumps({
  "client_id": os.environ["MCP_CLIENT_ID"],
  "client_secret": os.environ["MCP_CLIENT_SECRET"],
  "subject": os.environ.get("SUBJECT","user")
}, ensure_ascii=False, indent=2))
PY

command -v jq >/dev/null 2>&1 && jq . "$OUT" >/dev/null || true

echo "Wrote $OUT"
echo "client_id: $CLIENT_ID"
echo "client_secret: (hidden)"
echo "subject: $SUBJECT"
echo "Restart uvicorn in THIS shell so it sees MCP_CLIENT_ID/SECRET."

# restore -u
if [ $__had_u -eq 1 ]; then set -u; fi
unset __had_u
