"""
Day 33 — Multiprocessing Pools, Queues & Process Boundaries

Demonstrates:
- CPU-bound work distributed with multiprocessing.Pool
- Explicit communication through multiprocessing.Queue
- The process boundary between parent and worker processes
"""

from multiprocessing import Pool, Process, Queue


def square(number: int) -> int:
    """Return the square of a number in a worker process."""
    return number * number


def producer(queue: Queue, values: list[int]) -> None:
    """Publish values across the process boundary."""
    for value in values:
        queue.put(value)
    queue.put(None)


def consumer(queue: Queue) -> None:
    """Consume values until the producer sends a sentinel."""
    while True:
        value = queue.get()
        if value is None:
            break
        print(f"received {value}, squared = {value * value}")


def main() -> None:
    values = list(range(1, 5))

    # Pool is useful when independent CPU-bound tasks can be distributed
    # across multiple worker processes.
    with Pool(processes=2) as pool:
        results = pool.map(square, values)

    print(f"pool results: {results}")

    # Queue provides explicit inter-process communication. Objects are
    # serialized before crossing the process boundary.
    queue = Queue()
    producer_process = Process(target=producer, args=(queue, values))
    consumer_process = Process(target=consumer, args=(queue,))

    consumer_process.start()
    producer_process.start()

    producer_process.join()
    consumer_process.join()


if __name__ == "__main__":
    main()
