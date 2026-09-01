"""
Day 32 — Thread Safety

Demonstrates:
- Protecting shared state with Lock
- Re-entrant synchronization with RLock
- Waiting and notification with Condition
- Keeping synchronization boundaries small
"""

import threading


class ThreadSafeCounter:
    """Protect a shared counter with a Lock."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


class ReentrantCounter:
    """Use RLock when a locked method calls another locked method."""

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


class WorkQueue:
    """Coordinate a producer and consumer with a Condition."""

    def __init__(self) -> None:
        self._items: list[str] = []
        self._condition = threading.Condition()

    def put(self, item: str) -> None:
        with self._condition:
            self._items.append(item)
            self._condition.notify()

    def get(self) -> str:
        with self._condition:
            while not self._items:
                self._condition.wait()
            return self._items.pop(0)


def run_demo() -> None:
    counter = ThreadSafeCounter()

    threads = [
        threading.Thread(target=lambda: [counter.increment() for _ in range(1_000)])
        for _ in range(2)
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(f"Lock counter: {counter.value}")

    reentrant = ReentrantCounter()
    reentrant.increment()
    print(f"RLock counter: {reentrant.value}")

    queue = WorkQueue()
    consumer = threading.Thread(target=lambda: print(f"Consumed: {queue.get()}"))
    consumer.start()
    queue.put("expense-created")
    consumer.join()


if __name__ == "__main__":
    run_demo()
