"""
Phase 1 capstone: the "hello-MCP" server.

A minimal MCP server exposing two tools. Verified working on the official
MCP Python SDK v1.29 (mcp>=1.27,<2).

Run it directly (STDIO transport):
    python demo_server.py

Or explore it in the MCP Inspector:
    npx @modelcontextprotocol/inspector python demo_server.py
"""

from mcp.server.fastmcp import FastMCP

# Create the server. The name is what a client sees as `serverInfo`
# during the initialization handshake.
server = FastMCP("demo")


@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    # Type hints (a: float, b: float) become the tool's input schema:
    # both required numbers. The docstring becomes the tool description
    # that an LLM reads to decide when to use this tool.
    return a + b


@server.tool()
def greet(name: str) -> str:
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # run() starts the async event loop and listens over STDIO by default.
    server.run()
