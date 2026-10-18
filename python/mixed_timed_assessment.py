"""
Day 79 — Mixed Python timed assessment.

Focus: correctness, type hints, exception handling, generators, and concurrency
trade-offs. Run directly to execute the included smoke tests.
"""

from collections.abc import Callable, Iterator
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


def chunked(items: list[T], size: int) -> Iterator[list[T]]:
    """Yield consecutive chunks without producing empty trailing chunks."""
    if size <= 0:
        raise ValueError("size must be positive")
    for start in range(0, len(items), size):
        yield items[start : start + size]


def retry(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    retryable: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    """Retry selected transient failures, then re-raise the final exception."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(attempts):
        try:
            return operation()
        except retryable:
            if attempt == attempts - 1:
                raise
    raise RuntimeError("unreachable retry state")


def timed_call(
    operation: Callable[..., T], *args: object, **kwargs: object
) -> tuple[T, float]:
    """Return an operation's result and elapsed wall-clock seconds."""
    started = perf_counter()
    result = operation(*args, **kwargs)
    return result, perf_counter() - started


def run_smoke_tests() -> None:
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunked([], 3)) == []
    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("non-positive chunk size should fail")

    calls = 0

    def flaky_operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise TimeoutError("temporary failure")
        return "ok"

    assert retry(flaky_operation, attempts=3) == "ok"
    assert calls == 3
    result, elapsed = timed_call(sum, [1, 2, 3])
    assert result == 6
    assert elapsed >= 0


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 79 mixed Python smoke tests passed.")
