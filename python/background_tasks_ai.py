"""
Day 54 — Background Tasks for AI Workloads

A standard-library example of an async queue used to move long-running AI
work away from a latency-sensitive request path.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class AIJob:
    job_id: str
    operation: str
    payload: dict[str, str]


async def process_job(job: AIJob) -> None:
    """Represent an I/O-bound AI workload without calling a provider."""
    await asyncio.sleep(0)
    print(f"processed {job.operation}: {job.job_id} -> {job.payload}")


async def worker(queue: asyncio.Queue[AIJob | None]) -> None:
    while True:
        job = await queue.get()
        try:
            if job is None:
                return
            await process_job(job)
        finally:
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[AIJob | None] = asyncio.Queue()
    task = asyncio.create_task(worker(queue))

    # A request handler can enqueue ingestion/indexing work and return without
    # waiting for the complete AI workflow.
    await queue.put(
        AIJob(
            job_id="job-123",
            operation="embed-document",
            payload={"document_id": "doc-456"},
        )
    )
    await queue.put(
        AIJob(
            job_id="job-124",
            operation="refresh-index",
            payload={"dataset_version": "v3"},
        )
    )

    await queue.join()
    await queue.put(None)
    await task


if __name__ == "__main__":
    asyncio.run(main())
