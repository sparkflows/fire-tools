from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.mcp_jsonrpc import router as mcp_router

app = FastAPI(title="workflow-mcp-server", version="1.0.0")

# CORS (similar to application.properties)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

# JSON-RPC-like routes
app.include_router(mcp_router, prefix="")
