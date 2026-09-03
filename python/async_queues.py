"""
Day 34 — AsyncIO Queues & Producer/Consumer Pattern

Demonstrates an asyncio.Queue used to coordinate asynchronous producers and
consumers without blocking the event loop.
"""

from __future__ import annotations

import asyncio


async def producer(queue: asyncio.Queue[int | None], values: list[int]) -> None:
    """Publish values to the asynchronous work queue."""
    for value in values:
        await queue.put(value)
    await queue.put(None)


async def consumer(queue: asyncio.Queue[int | None]) -> None:
    """Process queued values until the producer sends a sentinel."""
    while True:
        value = await queue.get()
        try:
            if value is None:
                return

            await asyncio.sleep(0)
            print(f"processed {value}")
        finally:
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=2)

    producer_task = asyncio.create_task(producer(queue, [1, 2, 3, 4]))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.join()
    await consumer_task


if __name__ == "__main__":
    asyncio.run(main())
