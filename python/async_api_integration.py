"""
Day 51 — Async API Integration Review

Demonstrates an asynchronous HTTP boundary suitable for calling external
AI or backend APIs without blocking the event loop.

The example keeps the HTTP dependency optional so the module remains
inspectable in environments where httpx is not installed.
"""

from __future__ import annotations

from typing import Any, Optional


async def post_json(
    url: str,
    payload: dict[str, Any],
    headers: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """POST JSON asynchronously and return a validated JSON object."""
    try:
        import httpx
    except ImportError as exc:
        raise RuntimeError("Install httpx to run the async HTTP example.") from exc

    timeout = httpx.Timeout(15.0, connect=5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object from the API")

    return data


async def call_llm_api(
    url: str,
    model: str,
    prompt: str,
    api_key: str,
) -> dict[str, Any]:
    """Build a provider-neutral chat payload and send it asynchronously."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    return await post_json(
        url,
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )
