"""Day 85 — Python performance review helpers.

Use measurements before optimizing. These examples illustrate repeatable timing,
streaming processing, and bounded work rather than claiming universal speedups.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def measure_seconds(operation: Callable[[], R]) -> tuple[R, float]:
    """Run an operation once and return its result and elapsed wall time."""
    started = perf_counter()
    result = operation()
    return result, perf_counter() - started


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield bounded-size batches from an iterable."""
    if size < 1:
        raise ValueError("size must be at least one")
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def run_smoke_tests() -> None:
    result, elapsed = measure_seconds(lambda: sum(range(100)))
    assert result == 4950
    assert elapsed >= 0
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 3)) == []
    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid chunk size should fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 85 Python performance review checks passed.")
