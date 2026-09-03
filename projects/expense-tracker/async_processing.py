"""
Day 34 — Expense Tracker Async Processing

Provides an asyncio-based producer/consumer boundary for background expense
aggregation work. The worker runs blocking application/database handlers in
a worker thread so the event loop remains responsive.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import date
from typing import Callable


@dataclass(frozen=True)
class AggregationJob:
    """Describe one Expense Tracker aggregation request."""

    start_date: date
    end_date: date


class AsyncAggregationWorker:
    """Consume aggregation jobs without blocking the event loop."""

    def __init__(self, handler: Callable[[AggregationJob], None]) -> None:
        self._queue: asyncio.Queue[AggregationJob | None] = asyncio.Queue()
        self._handler = handler
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start the background consumer task."""
        self._task = asyncio.create_task(self._run())

    async def submit(self, job: AggregationJob) -> None:
        """Enqueue an aggregation request."""
        await self._queue.put(job)

    async def wait_for_completion(self) -> None:
        """Wait until all submitted jobs have been processed."""
        await self._queue.join()

    async def stop(self) -> None:
        """Stop the consumer after the current queue work is complete."""
        await self._queue.put(None)
        await self._task
        self._task = None

    async def _run(self) -> None:
        while True:
            job = await self._queue.get()
            try:
                if job is None:
                    return
                await asyncio.to_thread(self._handler, job)
            finally:
                self._queue.task_done()


def process_aggregation(job: AggregationJob) -> None:
    """Placeholder for the existing synchronous aggregation service."""
    print(f"aggregating expenses from {job.start_date} to {job.end_date}")


async def main() -> None:
    worker = AsyncAggregationWorker(process_aggregation)
    await worker.start()

    await worker.submit(
        AggregationJob(date(2026, 9, 1), date(2026, 9, 3))
    )
    await worker.submit(
        AggregationJob(date(2026, 8, 1), date(2026, 8, 31))
    )

    await worker.wait_for_completion()
    await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
