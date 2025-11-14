from fastapi import FastAPI
from mcp_json_rpc_controller import router as rpc_router

app = FastAPI()

app.include_router(rpc_router)
