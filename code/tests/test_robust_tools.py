"""
Test suite for the Phase 3 robust tools.

Proves the security guards actually work:
  - path traversal is blocked
  - SQL injection is treated as literal data (table survives)

Run from the repo root:
    cd code
    python -m pytest tests/test_robust_tools.py -v

Requires the phase3 package on the path; the conftest below handles it.
"""

import sqlite3
from pathlib import Path

import pytest

from phase3.robust_tools import read_file, find_user


def setup_module(module):
    """Arrange a safe_base dir with a file, and a test DB with one user."""
    Path("safe_base").mkdir(exist_ok=True)
    Path("safe_base/notes.txt").write_text("hello from inside the sandbox")
    conn = sqlite3.connect("app.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users VALUES (1, 'Avinash')")
    conn.commit()
    conn.close()


def test_reads_valid_file():
    assert read_file("notes.txt") == "hello from inside the sandbox"


def test_rejects_path_traversal():
    # The classic attack must be refused, not silently served.
    with pytest.raises(ValueError):
        read_file("../../etc/passwd")


def test_db_lookup_works():
    assert find_user("Avinash") == [{"id": 1, "name": "Avinash"}]


def test_sql_injection_is_treated_as_literal():
    # A crafted "name" must NOT execute; it should just match nothing.
    assert find_user("x'; DROP TABLE users;--") == []
    # And the table must still exist afterwards.
    conn = sqlite3.connect("app.db")
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    assert count == 1


def test_length_validation_rejects_empty():
    with pytest.raises(ValueError):
        find_user("")
