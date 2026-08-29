"""
Day 29 — Testing Async Python Code

Demonstrates:
- Async test structure
- AsyncMock
- Await assertions
- Testing async dependencies without real I/O
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock


async def fetch_user_name(user_id: int, client) -> str:
    """Fetch a user's name through an async dependency."""
    response = await client.get(f"/users/{user_id}")
    return response["name"]


async def demo() -> None:
    """Run a small async test-style example."""
    client = AsyncMock()
    client.get.return_value = {"id": 1, "name": "Alice"}

    name = await fetch_user_name(1, client)

    assert name == "Alice"
    client.get.assert_awaited_once_with("/users/1")


if __name__ == "__main__":
    asyncio.run(demo())
    print("Async testing example passed.")
