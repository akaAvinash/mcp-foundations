"""
Phase 3.2: Resources & Prompts.

Demonstrates the other two MCP primitives beyond tools:
  - a static resource (config://app)
  - a dynamic/templated resource (user://{user_id})
  - a parameterized prompt (summarize)

Verified working on MCP Python SDK v1.29.

Run:
    python resources_prompts.py
"""

from mcp.server.fastmcp import FastMCP

server = FastMCP("library")


@server.resource("config://app")
def app_config() -> str:
    """The application's current configuration as text (read-only)."""
    return "theme=dark\nlanguage=en\nversion=1.0"


@server.resource("user://{user_id}")
def get_user(user_id: str) -> str:
    """Return a user's public profile by id (templated resource)."""
    # If this touched a real datastore, apply the same input-validation
    # discipline as the tools in robust_tools.py.
    return f"Profile for user {user_id}"


@server.prompt()
def summarize(text: str, style: str = "bullets") -> str:
    """Produce a prompt that summarizes text in a chosen style."""
    # The server author encodes the good phrasing once; every user
    # gets it for free by invoking this prompt.
    return f"Summarize the following in {style}. Be concise and accurate:\n\n{text}"


if __name__ == "__main__":
    server.run()
