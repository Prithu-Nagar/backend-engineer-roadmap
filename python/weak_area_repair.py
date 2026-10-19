"""
Day 80 — Python weak-area repair.

Practice defensive input validation, generators, and bounded retries.
Run directly to execute smoke tests.
"""

from collections.abc import Callable, Iterator
from typing import TypeVar

T = TypeVar("T")


def positive_batches(items: list[T], batch_size: int) -> Iterator[list[T]]:
    """Yield non-empty batches; reject invalid batch sizes."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def retry_transient(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    retryable: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    """Retry only selected transient exceptions, then propagate the last one."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(attempts):
        try:
            return operation()
        except retryable:
            if attempt == attempts - 1:
                raise
    raise RuntimeError("unreachable retry state")


def run_smoke_tests() -> None:
    assert list(positive_batches([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(positive_batches([], 2)) == []
    try:
        list(positive_batches([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid batch size must fail")

    calls = 0

    def transient_operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 2:
            raise TimeoutError("temporary failure")
        return "recovered"

    assert retry_transient(transient_operation, attempts=2) == "recovered"
    assert calls == 2

    try:
        retry_transient(lambda: 1, attempts=0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero attempts must fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 80 Python weak-area repair passed.")
