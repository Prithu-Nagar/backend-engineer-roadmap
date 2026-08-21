"""
Day 21 — Async Flask Patterns

Topics:
- Async route handlers
- Awaiting I/O-bound work
- Running independent coroutines concurrently
- Avoiding blocking work inside async handlers

Requires Flask 2.x or newer.
"""

import asyncio

from flask import Flask, jsonify


app = Flask(__name__)


async def fetch_profile(user_id: int) -> dict:
    """Simulate an I/O-bound operation."""
    await asyncio.sleep(0.05)
    return {"user_id": user_id, "name": f"User {user_id}"}


async def fetch_preferences(user_id: int) -> dict:
    """Simulate a second independent I/O-bound operation."""
    await asyncio.sleep(0.05)
    return {"user_id": user_id, "theme": "dark"}


@app.get("/users/<int:user_id>/dashboard")
async def dashboard(user_id: int):
    """Run independent I/O operations concurrently."""

    profile, preferences = await asyncio.gather(
        fetch_profile(user_id),
        fetch_preferences(user_id),
    )

    return jsonify(
        {
            "profile": profile,
            "preferences": preferences,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
