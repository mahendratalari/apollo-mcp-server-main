import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from apollo_mcp.tools import register_all_tools
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette


class TrustAllHostsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.scope["headers"] = [
            (k, v) for k, v in request.scope["headers"]
            if k.lower() != b"host"
        ] + [(b"host", b"localhost")]
        return await call_next(request)


def create_server() -> FastMCP:
    mcp = FastMCP("Apollo MCP Server")
    register_all_tools(mcp)
    return mcp


def run_server():
    mcp = create_server()
    port = int(os.environ.get("PORT", 8000))
    app = mcp.sse_app()
    app.add_middleware(TrustAllHostsMiddleware)
    uvicorn.run(app, host="0.0.0.0", port=port)


_mcp = None


def get_server() -> FastMCP:
    global _mcp
    if _mcp is None:
        _mcp = create_server()
    return _mcp


if __name__ == "__main__":
    run_server()
