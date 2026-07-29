"""
Phase 3 course capstone: a small, complete, shippable MCP server.

A "notes" server that brings together everything in the course:
  - multiple tools with validation and structured errors
  - a path-traversal-safe file tool
  - a resource and a prompt
  - structured logging to stderr (never stdout on STDIO)
  - runnable over STDIO (default) or Streamable HTTP

Verified working on MCP Python SDK v1.29 (mcp>=1.27,<2).

Run over STDIO (local):
    python capstone_notes_server.py

Run over Streamable HTTP (network):  edit the __main__ block, or:
    (the SDK CLI)  uv run mcp dev capstone_notes_server.py

Environment variables:
    NOTES_DIR   directory the server may read/write notes in (default ./notes)
"""

import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Log to STDERR. On STDIO transport, STDOUT is the protocol wire, so
# logging there would corrupt the stream. Always log to stderr.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log = logging.getLogger("notes-server")

server = FastMCP("notes")

# Least privilege: the server can only reach its notes directory,
# never the whole filesystem. Scoped via an env var with a safe default.
NOTES_DIR = Path(os.getenv("NOTES_DIR", "./notes")).resolve()
NOTES_DIR.mkdir(parents=True, exist_ok=True)


def _safe_path(name: str) -> Path:
    """Resolve a note name to a path INSIDE NOTES_DIR, or raise."""
    target = (NOTES_DIR / name).resolve()
    if not target.is_relative_to(NOTES_DIR):
        raise ValueError("Access denied: name escapes the notes directory.")
    if not name.endswith(".txt"):
        raise ValueError("Note names must end with .txt")
    return target


@server.tool()
def write_note(name: str, content: str) -> str:
    """Create or overwrite a note. Name must end with .txt."""
    if not (1 <= len(name) <= 100):
        raise ValueError("name must be 1-100 characters.")
    target = _safe_path(name)
    target.write_text(content, encoding="utf-8")
    log.info("wrote note: %s (%d chars)", name, len(content))
    return f"Saved {name}"


@server.tool()
def read_note(name: str) -> str:
    """Read a note's contents by name."""
    target = _safe_path(name)
    if not target.is_file():
        raise ValueError(f"No such note: {name}")
    log.info("read note: %s", name)
    return target.read_text(encoding="utf-8")


@server.tool()
def list_notes() -> list[str]:
    """List all note names."""
    return sorted(p.name for p in NOTES_DIR.glob("*.txt"))


@server.tool()
def delete_note(name: str) -> str:
    """Delete a note by name."""
    target = _safe_path(name)
    if not target.is_file():
        raise ValueError(f"No such note: {name}")
    target.unlink()
    log.info("deleted note: %s", name)
    return f"Deleted {name}"


@server.resource("notes://index")
def notes_index() -> str:
    """A read-only index of all current notes."""
    names = sorted(p.name for p in NOTES_DIR.glob("*.txt"))
    return "\n".join(names) if names else "(no notes yet)"


@server.prompt()
def summarize_note(name: str, style: str = "bullets") -> str:
    """Produce a prompt that summarizes a named note in a chosen style."""
    return (
        f"Read the note '{name}' (use the read_note tool) and summarize it "
        f"in {style}. Be concise and accurate."
    )


if __name__ == "__main__":
    # STDIO (default) for local use:
    server.run()
    # For network use, run over Streamable HTTP instead:
    #   server.run(transport="streamable-http")
