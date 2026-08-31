"""
Day 31 — Database Connection Pooling

A small standard-library example that demonstrates the lifecycle of
a reusable connection pool without requiring a specific database driver.

The same principles apply to database-driver pools:
- Create a bounded number of connections.
- Borrow a connection for a short unit of work.
- Return it to the pool.
- Avoid creating a new connection for every request.
"""

from contextlib import contextmanager
from queue import LifoQueue
from typing import Iterator


class FakeConnection:
    """Represent a reusable database connection for demonstration."""

    def __init__(self, connection_id: int) -> None:
        self.connection_id = connection_id

    def execute(self, query: str) -> None:
        print(f"Connection {self.connection_id}: {query}")


class ConnectionPool:
    """A bounded pool of reusable connections."""

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("pool size must be positive")

        self._connections = LifoQueue(maxsize=size)

        for connection_id in range(1, size + 1):
            self._connections.put(FakeConnection(connection_id))

    @contextmanager
    def connection(self) -> Iterator[FakeConnection]:
        """Borrow a connection and always return it to the pool."""
        connection = self._connections.get()
        try:
            yield connection
        finally:
            self._connections.put(connection)

    @property
    def available(self) -> int:
        """Return the number of currently available connections."""
        return self._connections.qsize()


def run_demo() -> None:
    pool = ConnectionPool(size=2)

    print(f"Available connections: {pool.available}")

    with pool.connection() as connection:
        connection.execute("SELECT * FROM expenses")

    print(f"Available connections: {pool.available}")


if __name__ == "__main__":
    run_demo()
