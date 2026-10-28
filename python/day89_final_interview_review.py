"""Day 89 — Final Python interview review.

Small examples for common interview topics: generators, retry boundaries,
context managers, type-friendly data models, and deterministic tests.
"""

from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page:
    items: list[T]
    page: int
    page_size: int
    total_items: int


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
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
    started = perf_counter()
    yield lambda: perf_counter() - started


def paginate(items: list[T], page: int, page_size: int) -> Page:
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive")
    start = (page - 1) * page_size
    return Page(items=items[start:start + page_size], page=page,
                page_size=page_size, total_items=len(items))


def run_smoke_tests() -> None:
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 2)) == []
    assert paginate([1, 2, 3], 2, 2).items == [3]
    calls = 0

    def transient() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError("temporary")
        return "ready"

    assert retry_call(transient, attempts=2) == "ready"
    with elapsed_seconds() as elapsed:
        sum(range(100))
        assert elapsed() >= 0


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 89 Python review smoke tests passed.")
