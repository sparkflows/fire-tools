from dotenv import load_dotenv; load_dotenv()
from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from controllers.mcp_jsonrpc import router as mcp_router
from controllers.auth import router as auth_router
from security_jwt import require_access_token

app = FastAPI(title="workflow-mcp-server", version="1.0.0")

# Permissive CORS (mirror Java behavior)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Unprotected auth endpoints
app.include_router(auth_router)

# Protect ALL MCP endpoints with a Bearer (JWT) access token
secure_router = APIRouter(dependencies=[Depends(require_access_token)])
secure_router.include_router(mcp_router)
app.include_router(secure_router)
