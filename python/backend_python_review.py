"""Day 81 — Backend Python review: validation, pagination, and bounded retries."""
from collections.abc import Callable, Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")


def chunks(items: Sequence[T], size: int) -> Iterator[list[T]]:
    """Yield bounded batches while validating the requested batch size."""
    if size <= 0:
        raise ValueError("size must be positive")
    for start in range(0, len(items), size):
        yield list(items[start : start + size])


def parse_page(value: str | int, *, default: int = 1, maximum: int = 10_000) -> int:
    """Parse a positive page number and reject malformed or excessive values."""
    try:
        page = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("page must be an integer") from exc
    if page < 1 or page > maximum:
        raise ValueError(f"page must be between 1 and {maximum}")
    if default < 1:
        raise ValueError("default must be positive")
    return page


def call_with_retries(operation: Callable[[], T], attempts: int = 3) -> T:
    """Retry TimeoutError only; do not hide permanent failures."""
    if attempts < 1:
        raise ValueError("attempts must be at least one")
    for attempt in range(attempts):
        try:
            return operation()
        except TimeoutError:
            if attempt == attempts - 1:
                raise
    raise RuntimeError("unreachable retry state")


def run_smoke_tests() -> None:
    assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunks([], 3)) == []
    assert parse_page("4") == 4
    assert call_with_retries(lambda: "ok") == "ok"
    try:
        parse_page("0")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid page must fail")
    try:
        list(chunks([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid chunk size must fail")
    calls = 0
    def flaky() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError("temporary")
        return "recovered"
    assert call_with_retries(flaky, attempts=2) == "recovered"
    assert calls == 2


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 81 Python backend review passed.")
