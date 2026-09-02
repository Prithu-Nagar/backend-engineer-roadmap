"""
Day 33 — Background Jobs

A small standard-library example of separating HTTP request handling from
work that can be processed asynchronously by a background worker.
"""

from __future__ import annotations

from dataclasses import dataclass
from queue import Queue
from threading import Thread


@dataclass(frozen=True)
class Job:
    """Represent a unit of background work."""

    name: str
    payload: dict[str, object]


class BackgroundWorker:
    """Process queued jobs on a dedicated worker thread."""

    def __init__(self) -> None:
        self._jobs: Queue[Job | None] = Queue()
        self._thread = Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def submit(self, job: Job) -> None:
        self._jobs.put(job)

    def wait_for_completion(self) -> None:
        """Wait until all submitted jobs have been processed."""
        self._jobs.join()

    def stop(self) -> None:
        self._jobs.put(None)
        self._thread.join()

    def _run(self) -> None:
        while True:
            job = self._jobs.get()
            try:
                if job is None:
                    return
                self._process(job)
            finally:
                self._jobs.task_done()

    @staticmethod
    def _process(job: Job) -> None:
        print(f"processing background job: {job.name} -> {job.payload}")


def main() -> None:
    worker = BackgroundWorker()
    worker.start()

    # An API handler can enqueue work and return without performing the
    # potentially slower operation in the request path.
    worker.submit(Job("expense-aggregation", {"date": "2026-09-02"}))
    worker.submit(Job("expense-report", {"user_id": 42}))

    worker.wait_for_completion()
    worker.stop()


if __name__ == "__main__":
    main()
