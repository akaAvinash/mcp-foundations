"""
Phase 1.2: a tiny async warm-up (not an MCP server).

Shows why MCP is built on async: coroutines that WAIT (via await) yield
control so other work runs concurrently, instead of blocking.

Run:
    python async_example.py
"""

import asyncio


async def slow_add(a: int, b: int) -> int:
    """Pretend this is a slow I/O operation that yields while waiting."""
    await asyncio.sleep(1)  # yields control here, does not freeze the program
    return a + b


async def main() -> None:
    # Run three "slow" calls CONCURRENTLY. Because each spends its second
    # awaiting (yielding), all three overlap -> ~1s total, not ~3s.
    results = await asyncio.gather(
        slow_add(1, 1),
        slow_add(2, 2),
        slow_add(3, 3),
    )
    print("results:", results)  # [2, 4, 6]


if __name__ == "__main__":
    asyncio.run(main())
