"""
Python Threading Basics

Demonstrates:
- Creating threads
- Starting and joining threads
- Passing arguments to threads
- Protecting shared state with a lock
"""

import threading
import time


def worker(name: str, delay: float) -> None:
    """Simulate work performed by a thread."""
    print(f"{name} started")

    time.sleep(delay)

    print(f"{name} finished")


def run_basic_threads() -> None:
    """Create and run multiple worker threads."""
    threads = [
        threading.Thread(
            target=worker,
            args=("Worker-1", 1),
        ),
        threading.Thread(
            target=worker,
            args=("Worker-2", 1),
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def run_shared_counter() -> None:
    """Demonstrate protecting shared state with a Lock."""
    counter = 0
    lock = threading.Lock()

    def increment() -> None:
        nonlocal counter

        for _ in range(100_000):
            with lock:
                counter += 1

    threads = [
        threading.Thread(target=increment)
        for _ in range(2)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Final counter: {counter}")


if __name__ == "__main__":
    run_basic_threads()
    run_shared_counter()
