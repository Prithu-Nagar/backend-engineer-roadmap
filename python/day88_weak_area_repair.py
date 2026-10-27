"""Day 88 — Targeted Python repair after the Day 87 assessment.

Focus on contracts, deterministic tests, resource safety, and measuring
before optimizing. These small utilities are intentionally framework-free.
"""

from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield items in non-empty lists of at most size elements."""
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
    """Retry only declared transient errors; preserve the final exception."""
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
    """Provide elapsed monotonic time while the context is active."""
    started = perf_counter()
    yield lambda: perf_counter() - started


def normalize_page(page: int, page_size: int, maximum: int = 100) -> tuple[int, int]:
    """Validate one-based pagination and cap the requested page size."""
    if page < 1 or page_size < 1 or maximum < 1:
        raise ValueError("page, page_size, and maximum must be positive")
    return page, min(page_size, maximum)


def run_smoke_tests() -> None:
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 2)) == []
    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("zero chunk size should fail")

    calls = 0

    def transient() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError("temporary")
        return "ready"

    assert retry_call(transient, attempts=2) == "ready"
    assert normalize_page(1, 500) == (1, 100)
    with elapsed_seconds() as elapsed:
        sum(range(100))
        assert elapsed() >= 0


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 88 Python repair smoke tests passed.")
