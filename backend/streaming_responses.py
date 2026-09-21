"""
Day 52 — Streaming API Responses

A small FastAPI example for incremental HTTP responses. The same boundary can
be used for streamed LLM output, progress events, or large generated payloads.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="Streaming Response Example")


async def token_stream(tokens: list[str], delay: float = 0.0) -> AsyncIterator[str]:
    """Yield text fragments without buffering the complete response."""
    for token in tokens:
        if delay:
            await asyncio.sleep(delay)
        yield token


async def sse_stream(events: list[dict[str, Any]]) -> AsyncIterator[str]:
    """Yield Server-Sent Events as newline-delimited messages."""
    for event in events:
        payload = json.dumps(event, ensure_ascii=False)
        yield f"data: {payload}\n\n"


@app.get("/stream")
async def stream() -> StreamingResponse:
    return StreamingResponse(
        token_stream(["stream", "ing", " ", "response"], delay=0.01),
        media_type="text/plain; charset=utf-8",
    )


@app.get("/events")
async def events() -> StreamingResponse:
    return StreamingResponse(
        sse_stream([{"status": "started"}, {"status": "completed"}]),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
