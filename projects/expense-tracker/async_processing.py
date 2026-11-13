"""In-process background processing for Expense Tracker aggregation."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session


@dataclass(frozen=True)
class AggregationJob:
    """Describe one Expense Tracker aggregation request."""

    owner_id: int
    start_date: date
    end_date: date


AggregationResult = list[tuple[str, Decimal]]
AggregationHandler = Callable[[AggregationJob], AggregationResult]


@dataclass
class _QueuedJob:
    job: AggregationJob
    result: asyncio.Future[AggregationResult]


class AsyncAggregationWorker:
    """Run database aggregation jobs off-loop and return each job's outcome."""

    def __init__(self, handler: AggregationHandler) -> None:
        self._queue: asyncio.Queue[_QueuedJob | None] = asyncio.Queue()
        self._handler = handler
        self._task: asyncio.Task[None] | None = None
        self._stopping = False

    async def start(self) -> None:
        """Start the background consumer task."""
        if self._task is not None:
            raise RuntimeError("worker is already started")
        self._stopping = False
        self._task = asyncio.create_task(self._run())

    async def submit(
        self, job: AggregationJob
    ) -> asyncio.Future[AggregationResult]:
        """Enqueue a job and return a future for its result or raised error."""
        if self._task is None or self._task.done() or self._stopping:
            raise RuntimeError("worker is not accepting jobs")
        result = asyncio.get_running_loop().create_future()
        await self._queue.put(_QueuedJob(job, result))
        return result

    async def wait_for_completion(self) -> None:
        """Wait until all submitted jobs have been processed."""
        await self._queue.join()

    async def stop(self) -> None:
        """Stop the consumer after the current queue work is complete."""
        if self._task is None:
            raise RuntimeError("worker is not started")
        self._stopping = True
        await self._queue.join()
        await self._queue.put(None)
        await self._task
        self._task = None
        self._stopping = False

    async def _run(self) -> None:
        while True:
            queued = await self._queue.get()
            try:
                if queued is None:
                    return
                try:
                    result = await asyncio.to_thread(self._handler, queued.job)
                except Exception as error:  # noqa: BLE001 - forward job failures to the submitter
                    if not queued.result.done():
                        queued.result.set_exception(error)
                else:
                    if not queued.result.done():
                        queued.result.set_result(result)
            finally:
                self._queue.task_done()


def create_aggregation_handler(
    session_factory: Callable[[], Session],
) -> AggregationHandler:
    """Build a worker handler that owns and closes a session for each job."""
    from background_aggregation import aggregate_by_category

    def handle(job: AggregationJob) -> AggregationResult:
        with session_factory() as session:
            return aggregate_by_category(
                session,
                owner_id=job.owner_id,
                start_date=job.start_date,
                end_date=job.end_date,
            )

    return handle
