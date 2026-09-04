"""
Day 35 — Concurrency Pitfalls & Testing

Demonstrates common concurrency mistakes and a deterministic testing pattern.
The examples focus on synchronization boundaries rather than timing tricks.
"""

from __future__ import annotations

import threading
from unittest.mock import Mock


def increment_with_lock(iterations: int) -> int:
    """Illustrate shared mutable state that requires synchronization."""
    counter = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal counter
        for _ in range(iterations):
            with lock:
                counter += 1

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return counter


def test_worker_notification() -> None:
    """Test a concurrent collaborator without depending on sleep timing."""
    callback = Mock()
    event = threading.Event()

    def worker() -> None:
        callback("expense-created")
        event.set()

    thread = threading.Thread(target=worker)
    thread.start()

    assert event.wait(timeout=1), "worker did not finish in time"
    thread.join()
    callback.assert_called_once_with("expense-created")


if __name__ == "__main__":
    print(f"Safe synchronized result: {increment_with_lock(10_000)}")
    test_worker_notification()
    print("Concurrency test passed")
