"""
Day 52 — Streaming Responses

Demonstrates synchronous and asynchronous streaming boundaries that can feed
incremental HTTP responses without building the complete response in memory.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Iterator
from typing import Any


def stream_text(chunks: list[str]) -> Iterator[str]:
    """Yield text chunks one at a time."""
    for chunk in chunks:
        if chunk:
            yield chunk


async def stream_text_async(chunks: list[str], delay: float = 0.0) -> AsyncIterator[str]:
    """Yield text chunks asynchronously to model an I/O-backed producer."""
    for chunk in chunks:
        if delay:
            await asyncio.sleep(delay)
        if chunk:
            yield chunk


def to_sse(data: Any, event: str | None = None) -> str:
    """Encode one JSON value as a Server-Sent Events message."""
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_sse(events: list[dict[str, Any]]) -> AsyncIterator[str]:
    """Yield JSON events in SSE format."""
    for event in events:
        yield to_sse(event.get("data", event), event.get("event"))


if __name__ == "__main__":
    print("".join(stream_text(["Hello", " ", "streaming", "!"])))
