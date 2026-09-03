"""
Day 34 — Job Scheduling Concepts

A small standard-library scheduler that demonstrates delayed execution,
priority ordering, and explicit job state without tying the example to a
specific task queue framework.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
from itertools import count
from typing import Callable


@dataclass(frozen=True)
class ScheduledJob:
    """Represent a job waiting for its scheduled execution time."""

    name: str
    run_at: float
    priority: int = 0


class JobScheduler:
    """Store scheduled jobs in run-time and priority order."""

    def __init__(self) -> None:
        self._jobs: list[tuple[float, int, int, ScheduledJob]] = []
        self._sequence = count()

    def schedule(self, job: ScheduledJob) -> None:
        """Add a job to the scheduler."""
        heapq.heappush(
            self._jobs,
            (job.run_at, job.priority, next(self._sequence), job),
        )

    def run_due(self, now: float, handler: Callable[[ScheduledJob], None]) -> int:
        """Run jobs whose scheduled time has arrived and return the count."""
        processed = 0

        while self._jobs and self._jobs[0][0] <= now:
            _, _, _, job = heapq.heappop(self._jobs)
            handler(job)
            processed += 1

        return processed


def handle_job(job: ScheduledJob) -> None:
    print(f"running {job.name}")


def main() -> None:
    scheduler = JobScheduler()
    scheduler.schedule(ScheduledJob("daily-expense-report", run_at=10.0))
    scheduler.schedule(ScheduledJob("refresh-summary", run_at=10.0, priority=-1))
    scheduler.schedule(ScheduledJob("cleanup", run_at=20.0))

    scheduler.run_due(now=10.0, handler=handle_job)


if __name__ == "__main__":
    main()
