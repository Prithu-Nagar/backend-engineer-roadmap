"""
Day 12 - AsyncIO Tasks

Topics:
- asyncio.create_task()
- asyncio.gather()
- Timeouts
- Task cancellation
"""

import asyncio


async def fetch_data(name: str, delay: float) -> str:
    """
    Simulate an I/O-bound asynchronous operation.
    """
    print(f"Starting {name}")

    await asyncio.sleep(delay)

    print(f"Finished {name}")

    return f"{name} result"


async def run_tasks() -> None:
    """
    Create and run multiple asyncio tasks concurrently.
    """
    task_1 = asyncio.create_task(
        fetch_data("Task 1", 2)
    )

    task_2 = asyncio.create_task(
        fetch_data("Task 2", 1)
    )

    results = await asyncio.gather(
        task_1,
        task_2,
    )

    print("Results:", results)


async def run_with_timeout() -> None:
    """
    Demonstrate limiting the execution time of a coroutine.
    """
    try:
        result = await asyncio.wait_for(
            fetch_data("Timeout Task", 3),
            timeout=2,
        )

        print(result)

    except asyncio.TimeoutError:
        print("Task timed out")


async def run_with_cancellation() -> None:
    """
    Demonstrate cancelling an asyncio task.
    """
    task = asyncio.create_task(
        fetch_data("Cancellable Task", 5)
    )

    await asyncio.sleep(1)

    task.cancel()

    try:
        await task

    except asyncio.CancelledError:
        print("Task was cancelled")


async def main() -> None:
    print("Running concurrent tasks:")
    await run_tasks()

    print("\nRunning task with timeout:")
    await run_with_timeout()

    print("\nRunning cancellable task:")
    await run_with_cancellation()


if __name__ == "__main__":
    asyncio.run(main())
