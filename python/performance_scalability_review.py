"""
Day 69 — Performance and Scalability Review

Provider-neutral patterns for measuring hot paths, bounding work, and choosing
scaling strategies before optimizing a Python backend.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PerformanceSnapshot:
    """Small set of measurements used during a performance review."""

    operation: str
    item_count: int
    elapsed_ms: float


def measure(
    operation: str,
    items: Iterable[T],
    handler: Callable[[T], object],
) -> PerformanceSnapshot:
    """Measure one batch without hiding the work performed by the handler."""
    materialized = list(items)
    started = perf_counter()

    for item in materialized:
        handler(item)

    elapsed_ms = (perf_counter() - started) * 1000
    return PerformanceSnapshot(
        operation=operation,
        item_count=len(materialized),
        elapsed_ms=elapsed_ms,
    )


def choose_scaling_strategy(
    *,
    cpu_bound: bool,
    shared_state_required: bool,
    io_bound: bool,
    workload_is_bursty: bool,
) -> str:
    """Choose a first scaling direction from workload characteristics."""
    if cpu_bound:
        return (
            "profile first, then consider process-based parallelism "
            "or horizontal scaling"
        )

    if io_bound and not shared_state_required:
        return (
            "use bounded async/concurrent I/O and scale service "
            "instances horizontally"
        )

    if workload_is_bursty:
        return "use queues or workers to smooth bursts and bound request-path work"

    return "optimize the measured hot path, then scale horizontally when needed"


def batch_work(items: Iterable[T], batch_size: int) -> list[list[T]]:
    """Split work into bounded batches to avoid unbounded memory growth."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    batches: list[list[T]] = []
    current: list[T] = []

    for item in items:
        current.append(item)
        if len(current) == batch_size:
            batches.append(current)
            current = []

    if current:
        batches.append(current)

    return batches


if __name__ == "__main__":
    snapshot = measure("square", range(1_000), lambda value: value * value)
    print(snapshot)
    print(
        choose_scaling_strategy(
            cpu_bound=False,
            shared_state_required=False,
            io_bound=True,
            workload_is_bursty=False,
        )
    )
    print(batch_work(range(7), 3))
