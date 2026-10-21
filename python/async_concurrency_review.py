"""Day 82: AsyncIO and concurrency review for backend interview practice.

The examples are standard-library only. Run directly for smoke tests.
"""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from time import monotonic
from typing import TypeVar

T = TypeVar("T")


async def bounded_map(
    items: list[int],
    operation: Callable[[int], Awaitable[T]],
    concurrency: int = 3,
) -> list[T]:
    """Run async operations with a concurrency limit and preserve input order."""
    if concurrency < 1:
        raise ValueError("concurrency must be at least one")
    semaphore = asyncio.Semaphore(concurrency)

    async def run_one(item: int) -> T:
        async with semaphore:
            return await operation(item)

    return await asyncio.gather(*(run_one(item) for item in items))


async def delayed_double(value: int, delay: float = 0.001) -> int:
    await asyncio.sleep(delay)
    return value * 2


async def run_smoke_tests() -> None:
    assert await bounded_map([1, 2, 3], delayed_double, concurrency=2) == [2, 4, 6]
    assert await bounded_map([], delayed_double) == []
    try:
        await bounded_map([1], delayed_double, concurrency=0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero concurrency must fail")

    started = monotonic()
    results = await bounded_map(
        [1, 2, 3, 4],
        lambda value: delayed_double(value, delay=0.01),
        concurrency=2,
    )
    elapsed = monotonic() - started
    assert results == [2, 4, 6, 8]
    # Timing is a loose sanity check, not a performance benchmark.
    assert elapsed < 1.0


if __name__ == "__main__":
    asyncio.run(run_smoke_tests())
    print("Day 82 AsyncIO/concurrency review passed.")
