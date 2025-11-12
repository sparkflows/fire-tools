# Server Setup

## 1) Python env & dependencies

Create a fresh **Linux** venv on the VM and install deps:
```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip jq unzip

cd /home/sparkflows/sparkflows-MCP-Python
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# ensure these exist (add to requirements.txt if missing)
pip install PyJWT uvicorn fastapi
deactivate

```

---

## 2) Configure authentication (.env)

Create `/home/sparkflows/sparkflows-MCP-Python/.env`:
```bash
cat > .env <<'EOF'
MCP_JWT_ISS=sparkflows-mcp
MCP_JWT_AUD=mcp-clients
# Use a long, random base64 secret (keep this stable)
MCP_JWT_SECRET=REPLACE_WITH_LONG_BASE64_RANDOM

# These must match the client credentials you give to callers
MCP_CLIENT_ID=REPLACE_WITH_CLIENT_ID
MCP_CLIENT_SECRET=REPLACE_WITH_CLIENT_SECRET
EOF
```

Optional helper scripts (if present):
```bash
chmod +x server-setup/setup_auth.sh server-setup/create_client.sh
# Populate JWT_* quickly (still edit .env CLIENT_ID/SECRET to match)
./server-setup/setup_auth.sh
./server-setup/create_client.sh --subject "dhruv"
# Then copy values into .env
```

---

## 3) Install systemd service

Create/update `/etc/systemd/system/sparkflows-mcp.service`:
```bash
sudo tee /etc/systemd/system/sparkflows-mcp.service >/dev/null <<'UNIT'
[Unit]
Description=Sparkflows MCP (FastAPI/Uvicorn)
After=network.target

[Service]
User=sparkflows
Group=sparkflows
WorkingDirectory=/home/sparkflows/sparkflows-MCP-Python
EnvironmentFile=/home/sparkflows/sparkflows-MCP-Python/.env
ExecStart=/home/sparkflows/sparkflows-MCP-Python/.venv/bin/python -m uvicorn app:app \
  --host 0.0.0.0 --port 8090 \
  --env-file /home/sparkflows/sparkflows-MCP-Python/.env \
  --app-dir /home/sparkflows/sparkflows-MCP-Python
Restart=always
RestartSec=3
# Hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
# Running from /home, so allow access
ProtectHome=false

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable sparkflows-mcp
sudo systemctl restart sparkflows-mcp
sudo systemctl status sparkflows-mcp --no-pager
```

You should see **active (running)**.

---

## 6) Smoke test

From the VM:
```bash
# Confirm env visible to the server
curl -s http://localhost:8090/auth/debug | jq

# Request token (body must match MCP_CLIENT_ID/SECRET in .env)
cat > /tmp/client-credentials.json <<'JSON'
{
  "client_id": "REPLACE_WITH_CLIENT_ID",
  "client_secret": "REPLACE_WITH_CLIENT_SECRET",
  "subject": "dhruv"
}
JSON

TOK=$(curl -s http://localhost:8090/auth/token \
  -H 'Content-Type: application/json' \
  -d @/tmp/client-credentials.json)
echo "$TOK" | jq .
ACC=$(echo "$TOK" | jq -r .access_token)

curl -s http://localhost:8090/ \
  -H "Authorization: Bearer $ACC" \
  -H 'Content-Type: application/json' \
  -d '{"id":"1","jsonrpc":"2.0","method":"initialize","params":{}}' | jq .

```

From your client (replace IP):
```bash
TOK=$(curl -s http://<VM_IP>:8090/auth/token \
  -H 'Content-Type: application/json' \
  -d @server-setup/client-credentials.json)
ACC=$(echo "$TOK" | jq -r .access_token)

curl -s http://<VM_IP>:8090/ \
  -H "Authorization: Bearer $ACC" \
  -H 'Content-Type: application/json' \
  -d '{"id":"1","jsonrpc":"2.0","method":"initialize","params":{}}' | jq .
```

---

## Daily operations
```bash
# logs
journalctl -u sparkflows-mcp -f

# restart after code or .env changes
sudo systemctl restart sparkflows-mcp

# status
sudo systemctl status sparkflows-mcp --no-pager
```

---

## On Code Update
```bash
sudo systemctl stop sparkflows-mcp
cd /home/sparkflows/sparkflows-MCP-Python
# EITHER: git pull
# OR: replace with a new zip then unzip here
. .venv/bin/activate && pip install -r requirements.txt && deactivate
sudo systemctl start sparkflows-mcp

```

> If you changed dependencies, always re-run `pip install -r requirements.txt`.  
> If you changed `MCP_CLIENT_ID/SECRET` or `MCP_JWT_*`, update `.env` and restart.

---


## Troubleshooting quick hits

- **401 “Invalid client credentials” on `/auth/token`**  
    `.env` `MCP_CLIENT_ID/SECRET` don’t match the POST body. Align them and restart.
- **“Missing bearer token” on JSON-RPC**  
    Your `Authorization: Bearer` header is empty or missing. Obtain `access_token` and include it.
- **Service won’t start; “Exec format error”**  
    Delete a Mac-copied venv and recreate on the VM:
```bash
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate && pip install -r requirements.txt && deactivate
```
- **Import errors / not finding `app.py`**  
    Make sure `WorkingDirectory`, `EnvironmentFile`, and `--app-dir` in the unit file all point to `/home/sparkflows/sparkflows-MCP-Python`.
- **Port in use**
    `sudo ss -lntp '( sport = :8090 )'`

---
