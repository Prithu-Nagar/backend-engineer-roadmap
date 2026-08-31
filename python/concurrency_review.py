"""
Day 31 — Concurrency Review

Demonstrates:
- Race conditions caused by unsynchronized shared state
- Protecting shared state with Lock
- RLock for re-entrant locking
- Condition variables for coordination

The examples use threads and intentionally small critical sections so the
synchronization boundary is easy to identify.
"""

import threading


def increment_without_lock(iterations: int) -> int:
    """Demonstrate why shared mutable state needs synchronization."""
    counter = 0

    def increment() -> None:
        nonlocal counter
        for _ in range(iterations):
            counter += 1

    threads = [threading.Thread(target=increment) for _ in range(2)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return counter


def increment_with_lock(iterations: int) -> int:
    """Protect shared state with a Lock."""
    counter = 0
    lock = threading.Lock()

    def increment() -> None:
        nonlocal counter
        for _ in range(iterations):
            with lock:
                counter += 1

    threads = [threading.Thread(target=increment) for _ in range(2)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return counter


class SafeCounter:
    """Use RLock when a method may re-enter another locked method."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.RLock()

    def increment(self) -> None:
        with self._lock:
            self._increment_internal()

    def _increment_internal(self) -> None:
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


def run_condition_example() -> None:
    """Coordinate a worker and producer using a Condition."""
    condition = threading.Condition()
    ready = False

    def consumer() -> None:
        nonlocal ready

        with condition:
            while not ready:
                condition.wait()
            print("Consumer received the signal")

    def producer() -> None:
        nonlocal ready

        with condition:
            ready = True
            condition.notify()

    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()


if __name__ == "__main__":
    expected = 200_000
    print(f"With lock: {increment_with_lock(100_000)} / {expected}")

    counter = SafeCounter()
    counter.increment()
    print(f"RLock counter: {counter.value}")

    run_condition_example()
