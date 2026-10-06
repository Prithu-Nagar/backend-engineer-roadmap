"""
Day 67 — Concurrency Design Review

Framework-neutral examples for reviewing concurrency boundaries in backend
services. The examples emphasize ownership, bounded parallelism, and avoiding
unsafe shared mutable state.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from threading import Lock
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class Counter:
    """A shared counter whose mutation is protected by an explicit lock."""

    value: int = 0

    def __post_init__(self) -> None:
        self._lock = Lock()

    def increment(self, amount: int = 1) -> int:
        with self._lock:
            self.value += amount
            return self.value


def map_bounded(
    items: Iterable[T],
    operation: Callable[[T], R],
    max_workers: int = 4,
) -> list[R]:
    """Run independent I/O-oriented work with a bounded worker pool."""

    if max_workers <= 0:
        raise ValueError("max_workers must be positive")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures: list[Future[R]] = [
            executor.submit(operation, item) for item in items
        ]
        return [future.result() for future in futures]


def main() -> None:
    counter = Counter()
    for _ in range(3):
        counter.increment()

    results = map_bounded(
        range(5),
        lambda value: value * value,
        max_workers=2,
    )

    print("counter:", counter.value)
    print("results:", results)


if __name__ == "__main__":
    main()
