# MCP Foundations

A hands-on course that takes you from zero to a **solid working foundation** in the Model Context Protocol (MCP) — enough to build real MCP servers, understand the protocol deeply, and extend confidently from there.

This is a **foundation, not an encyclopedia**: three phases, finishable in a few weeks, with runnable and tested code at every step.

> **Provenance & honesty note:** This course was assembled with heavy use of AI assistance and then curated, restructured, and verified. All code in `code/` was executed and tested against the official MCP Python SDK **v1.29** before being committed (see [Testing](#testing)). Version-specific details are hedged with an "inspect, don't memorize" approach because MCP moves fast — always verify against your installed SDK.

## Who this is for

Software engineers, QA engineers, SDETs, backend developers, and AI engineers who know Python, OOP, REST APIs, Git, and basic async — and want to genuinely understand MCP rather than copy-paste a quickstart.

## What you'll be able to do

- Explain what MCP is and why it exists (the M×N → M+N integration problem)
- Read, trace, and **debug the MCP wire protocol** (JSON-RPC) by hand
- Build MCP servers with tools, resources, and prompts
- Validate inputs and avoid the classic security holes (path traversal, SQL injection)
- Choose a transport (STDIO vs Streamable HTTP)
- Test, log, and ship a small real server you designed

## Course structure

| Phase | Focus | Lessons |
|-------|-------|---------|
| **1 — Foundations & Your First Server** | Concepts + build a working server | 3 |
| **2 — The Protocol** *(the core)* | JSON-RPC, handshake, discovery, debugging | 5 |
| **3 — Building Real MCP Servers** | Robust tools, resources, prompts, security, shipping | 3 |

Full lesson text lives in [`course/`](course/). Runnable code lives in [`code/`](code/).

## Quick start

```bash
# 1. Clone and enter
git clone https://github.com/akaAvinash/mcp-foundations.git
cd mcp-foundations

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install (pinned to the SDK v1.x line this course targets)
pip install -r requirements.txt

# 4. Run your first server in the MCP Inspector
npx @modelcontextprotocol/inspector python code/phase1/demo_server.py
```

> **Important version note:** `pip install mcp` on its own now installs **v2.x**, which has a **different API** (no `mcp.server.fastmcp`). This course targets **v1.x**. Always install via `requirements.txt` (which pins `mcp>=1.27,<2`) or pin it yourself.

## The code

| File | What it is | Tested |
|------|-----------|:------:|
| `code/phase1/demo_server.py` | The "hello-MCP" server: two tools | ✅ |
| `code/phase1/async_example.py` | Async warm-up showing concurrency | ✅ |
| `code/phase3/robust_tools.py` | Path-traversal-safe file tool + injection-safe DB tool | ✅ |
| `code/phase3/resources_prompts.py` | Static + dynamic resources and a prompt | ✅ |
| `code/phase3/capstone_notes_server.py` | The course capstone: a complete notes server | ✅ |
| `code/tests/test_robust_tools.py` | Proves the security guards actually work | ✅ |

## Testing

All code is verified. To run the tests yourself:

```bash
cd code
python -m pytest tests/ -v
```

Expected: 5 passed — including a test that a path-traversal attempt is **blocked** and that a SQL-injection string is treated as **literal data** (the table survives).

## A note on accuracy

MCP is evolving quickly. This course:
- Was tested against **MCP Python SDK v1.29** (July 2026).
- Teaches you to **inspect the SDK** (`dir()`, `help()`, `inspect.signature()`) rather than memorize APIs, so you stay correct across versions.
- Pins dependencies so the examples run as written.

If something doesn't match your installed SDK, trust your inspection — and consider opening an issue or PR.

## License

MIT — see [LICENSE](LICENSE).
