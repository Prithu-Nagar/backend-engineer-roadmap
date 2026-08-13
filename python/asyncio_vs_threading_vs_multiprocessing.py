"""
AsyncIO vs Threading vs Multiprocessing

Day 13 focus:
- AsyncIO
- Threading
- Multiprocessing
- When to use each concurrency model
"""

import asyncio
import multiprocessing
import threading
import time


def blocking_task(name: str, duration: float) -> None:
    """Simulate a blocking I/O-bound task."""
    print(f"{name} started")
    time.sleep(duration)
    print(f"{name} completed")


def run_with_threading() -> None:
    """Run multiple blocking tasks concurrently using threads."""
    threads = []

    for number in range(3):
        thread = threading.Thread(
            target=blocking_task,
            args=(f"Thread {number + 1}", 1),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def cpu_bound_task(number: int) -> int:
    """Perform a CPU-intensive calculation."""
    result = 0

    for value in range(number):
        result += value * value

    return result


def run_with_multiprocessing() -> None:
    """Run CPU-bound tasks using multiple processes."""
    numbers = [100_000, 150_000, 200_000]

    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_bound_task, numbers)

    print("Multiprocessing results:", results)


async def async_task(name: str, duration: float) -> None:
    """Simulate an asynchronous I/O-bound task."""
    print(f"{name} started")
    await asyncio.sleep(duration)
    print(f"{name} completed")


async def run_with_asyncio() -> None:
    """Run multiple asynchronous tasks concurrently."""
    tasks = [
        async_task("Async Task 1", 1),
        async_task("Async Task 2", 1),
        async_task("Async Task 3", 1),
    ]

    await asyncio.gather(*tasks)


def explain_when_to_use_each() -> None:
    """Print a simple guide for choosing a concurrency model."""
    print(
        """
        AsyncIO:
            Best suited for I/O-bound workloads when the libraries
            being used support asynchronous operations.

        Threading:
            Useful for I/O-bound workloads involving blocking
            operations or libraries that are not async-native.

        Multiprocessing:
            Useful for CPU-bound workloads where work can be
            distributed across multiple processes.
        """
    )


if __name__ == "__main__":
    print("=== Threading ===")
    run_with_threading()

    print("\n=== Multiprocessing ===")
    run_with_multiprocessing()

    print("\n=== AsyncIO ===")
    asyncio.run(run_with_asyncio())

    print("\n=== When to Use Each ===")
    explain_when_to_use_each()