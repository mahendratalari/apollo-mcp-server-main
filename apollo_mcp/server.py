import os
from mcp.server.fastmcp import FastMCP
from apollo_mcp.tools import register_all_tools


def create_server() -> FastMCP:
    mcp = FastMCP("Apollo MCP Server")
    register_all_tools(mcp)
    return mcp


def run_server():
    mcp = create_server()
    port = int(os.environ.get("PORT", 8000))
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port
    mcp.settings.allowed_hosts = ["*"]
    mcp.run(transport="sse")


_mcp = None


def get_server() -> FastMCP:
    global _mcp
    if _mcp is None:
        _mcp = create_server()
    return _mcp


if __name__ == "__main__":
    run_server()
