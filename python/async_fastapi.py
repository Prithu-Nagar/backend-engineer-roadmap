"""
Day 28 — Async FastAPI Endpoints

Demonstrates:
- async FastAPI endpoints
- awaiting I/O-bound work
- concurrent independent operations
- keeping blocking work out of the async request path

The I/O operations are simulated with asyncio.sleep() so the example
does not require an external service.
"""

import asyncio

from fastapi import FastAPI


app = FastAPI(title="Async FastAPI Example")


async def fetch_profile(user_id: int) -> dict[str, object]:
    """Simulate an asynchronous profile lookup."""
    await asyncio.sleep(0.05)
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
    }


async def fetch_preferences(user_id: int) -> dict[str, object]:
    """Simulate an independent asynchronous lookup."""
    await asyncio.sleep(0.05)
    return {
        "user_id": user_id,
        "theme": "dark",
    }


@app.get("/users/{user_id}/dashboard")
async def get_dashboard(user_id: int) -> dict[str, object]:
    """Run independent I/O operations concurrently."""
    profile, preferences = await asyncio.gather(
        fetch_profile(user_id),
        fetch_preferences(user_id),
    )

    return {
        "profile": profile,
        "preferences": preferences,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
