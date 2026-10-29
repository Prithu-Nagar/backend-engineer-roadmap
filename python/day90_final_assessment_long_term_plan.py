"""Day 90 — Final Python assessment and long-term practice plan.

Examples cover typed data models, lazy iteration, selective retries, context
management, and explicit benchmark records.
"""

from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class AssessmentResult:
    topic: str
    score: int
    maximum: int
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.topic.strip():
            raise ValueError("topic is required")
        if self.maximum <= 0 or not 0 <= self.score <= self.maximum:
            raise ValueError("score must be between zero and maximum")


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


def run_smoke_tests() -> None:
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 2)) == []
    assert AssessmentResult("Python", 8, 10).score == 8
    try:
        AssessmentResult("Python", 11, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("scores above maximum must fail")
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
    print("Day 90 Python assessment smoke tests passed.")
