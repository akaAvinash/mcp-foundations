"""
Phase 3.1: Building Robust Tools.

Demonstrates input validation, structured errors, path-traversal-safe
file reading, and SQL-injection-safe database queries.

Both security defenses in this file are verified by the test suite in
code/tests/test_robust_tools.py (path traversal is blocked; SQL injection
is treated as literal data).

Run:
    python robust_tools.py
"""

from pathlib import Path
import sqlite3

from mcp.server.fastmcp import FastMCP

server = FastMCP("robust")

# The sandbox: the ONLY directory read_file is allowed to read from.
# .resolve() makes it absolute and canonical.
BASE_DIR = Path("./safe_base").resolve()


@server.tool()
def read_file(relative_path: str) -> str:
    """Read a text file from the safe directory and return its contents."""
    # 1. Resolve the requested path to a canonical absolute path.
    #    This collapses any '../' sequences to a real location.
    target = (BASE_DIR / relative_path).resolve()

    # 2. Path-traversal guard: the resolved target must stay inside BASE_DIR.
    #    If relative_path was '../../etc/passwd', target now points outside
    #    and we refuse. This one check closes the path-traversal hole.
    if not target.is_relative_to(BASE_DIR):
        raise ValueError("Access denied: path escapes the allowed directory.")

    # 3. Validate it exists and is a file.
    if not target.is_file():
        raise ValueError(f"Not a readable file: {relative_path}")

    # 4. Only now do the work.
    return target.read_text(encoding="utf-8")


@server.tool()
def find_user(name: str) -> list[dict]:
    """Look up users by exact name."""
    # Validate input length first, before touching the database.
    if not (1 <= len(name) <= 100):
        raise ValueError("name must be 1-100 characters.")

    conn = sqlite3.connect("app.db")
    # Parameterized query: '?' is a placeholder and `name` is passed
    # SEPARATELY, so the database treats it strictly as data, never as SQL.
    # This is what prevents SQL injection.
    rows = conn.execute(
        "SELECT id, name FROM users WHERE name = ?", (name,)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1]} for r in rows]


if __name__ == "__main__":
    server.run()
