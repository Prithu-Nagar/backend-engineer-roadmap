"""Day 87 — Full timed Python assessment.

Focus on clear contracts, type hints, exception safety, resource cleanup,
and testable behavior. Suggested time: 45 minutes.
"""

from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield non-empty chunks; reject invalid chunk sizes."""
    if size <= 0:
        raise ValueError("size must be positive")
    chunk: list[T] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def retry_call(
    operation: Callable[[], T],
    attempts: int = 3,
    retryable: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    """Retry only explicitly retryable exceptions."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    for attempt in range(attempts):
        try:
            return operation()
        except retryable:
            if attempt == attempts - 1:
                raise
    raise RuntimeError("unreachable retry state")


@contextmanager
def elapsed_seconds() -> Iterator[Callable[[], float]]:
    """Expose elapsed wall-clock time while a block is running."""
    started = perf_counter()
    yield lambda: perf_counter() - started


def run_smoke_tests() -> None:
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 3)) == []
    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid chunk size must fail")

    calls = 0

    def flaky() -> str:
        nonlocal calls
        calls += 1
        if calls < 2:
            raise TimeoutError("temporary")
        return "ok"

    assert retry_call(flaky, attempts=2) == "ok"
    with elapsed_seconds() as elapsed:
        sum(range(100))
        assert elapsed() >= 0


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 87 Python assessment smoke tests passed.")
