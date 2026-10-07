"""Review async architecture choices for backend services.

The example keeps concurrency policy separate from business logic and shows
bounded task fan-out, cancellation, timeout handling, and deterministic result
collection.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def run_bounded(
    items: Sequence[T],
    worker: Callable[[T], Awaitable[R]],
    *,
    concurrency: int,
    timeout: float,
) -> list[R]:
    """Run independent async work with an explicit concurrency limit."""
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    semaphore = asyncio.Semaphore(concurrency)

    async def guarded(item: T) -> R:
        async with semaphore:
            return await asyncio.wait_for(worker(item), timeout=timeout)

    tasks = [asyncio.create_task(guarded(item)) for item in items]

    try:
        return list(await asyncio.gather(*tasks))
    except Exception:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise


async def fetch_profile(user_id: int) -> str:
    """Represent an independent I/O-bound operation."""
    await asyncio.sleep(0)
    return f"profile:{user_id}"


async def main() -> None:
    """Demonstrate a bounded async workflow."""
    results = await run_bounded(
        range(1, 5),
        fetch_profile,
        concurrency=2,
        timeout=1.0,
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
