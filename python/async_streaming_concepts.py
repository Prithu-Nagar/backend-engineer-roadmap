"""
Day 53 — Async Streaming Concepts

Demonstrates async generators, cooperative cancellation, and bounded
producer/consumer flow for streaming workloads.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator


async def token_stream(tokens: list[str], delay: float = 0.0) -> AsyncIterator[str]:
    """Yield chunks without blocking the event loop."""
    for token in tokens:
        if delay:
            await asyncio.sleep(delay)
        yield token


async def consume_stream(
    stream: AsyncIterator[str],
    stop_after: int | None = None,
) -> list[str]:
    """Consume a stream and stop cooperatively when requested."""
    received: list[str] = []

    async for chunk in stream:
        received.append(chunk)
        if stop_after is not None and len(received) >= stop_after:
            break

    return received


async def bounded_producer(
    queue: asyncio.Queue[str | None],
    chunks: list[str],
) -> None:
    """Put chunks into a bounded queue to make producer pressure explicit."""
    for chunk in chunks:
        await queue.put(chunk)
    await queue.put(None)


async def bounded_consumer(queue: asyncio.Queue[str | None]) -> list[str]:
    """Read until the producer sends the completion sentinel."""
    received: list[str] = []

    while True:
        chunk = await queue.get()
        try:
            if chunk is None:
                return received
            received.append(chunk)
        finally:
            queue.task_done()


async def demo() -> None:
    stream = token_stream(["RAG", " ", "stream", " ", "ready"], delay=0.01)
    print(await consume_stream(stream))

    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=2)
    producer = asyncio.create_task(bounded_producer(queue, ["a", "b", "c"]))
    consumer = asyncio.create_task(bounded_consumer(queue))

    await producer
    print(await consumer)


if __name__ == "__main__":
    asyncio.run(demo())
