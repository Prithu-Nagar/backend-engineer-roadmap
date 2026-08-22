"""
Day 22 — AsyncIO HTTP and Database Workload Concepts

This file demonstrates the orchestration pattern used when an async
backend endpoint needs to coordinate independent HTTP and database-like
I/O operations.

The examples use asyncio.sleep() to simulate external I/O so the file
can run without third-party services.
"""

import asyncio
from dataclasses import dataclass


@dataclass
class UserProfile:
    user_id: int
    name: str


async def fetch_user_profile(user_id: int) -> UserProfile:
    """Simulate an asynchronous HTTP request."""
    await asyncio.sleep(0.05)
    return UserProfile(user_id=user_id, name=f"User {user_id}")


async def fetch_recent_orders(user_id: int) -> list[dict]:
    """Simulate an asynchronous database query."""
    await asyncio.sleep(0.05)
    return [
        {"order_id": 101, "user_id": user_id, "status": "completed"},
        {"order_id": 102, "user_id": user_id, "status": "processing"},
    ]


async def build_dashboard(user_id: int) -> dict:
    """
    Run independent I/O operations concurrently.

    Real applications should use async-compatible HTTP clients and
    database drivers rather than blocking synchronous libraries.
    """

    profile_task = asyncio.create_task(fetch_user_profile(user_id))
    orders_task = asyncio.create_task(fetch_recent_orders(user_id))

    profile, orders = await asyncio.gather(profile_task, orders_task)

    return {
        "profile": {
            "user_id": profile.user_id,
            "name": profile.name,
        },
        "orders": orders,
    }


async def main() -> None:
    dashboard = await build_dashboard(42)
    print(dashboard)


if __name__ == "__main__":
    asyncio.run(main())
