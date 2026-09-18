"""
Day 49 — LRU Cache

Mixed timed-review problem: combine a hash map with a doubly linked list so
lookup, insertion, and eviction remain O(1).
"""

from __future__ import annotations


class _Node:
    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    """Least-recently-used cache with O(1) get and put operations."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self.cache: dict[int, _Node] = {}
        self.left = _Node()   # least-recently-used sentinel
        self.right = _Node()  # most-recently-used sentinel
        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node: _Node) -> None:
        previous = node.prev
        following = node.next
        if previous is None or following is None:
            return
        previous.next = following
        following.prev = previous

    def _insert_at_right(self, node: _Node) -> None:
        previous = self.right.prev
        if previous is None:
            return
        previous.next = node
        node.prev = previous
        node.next = self.right
        self.right.prev = node

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if node is None:
            return -1

        self._remove(node)
        self._insert_at_right(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        existing = self.cache.get(key)
        if existing is not None:
            self._remove(existing)
            del self.cache[key]

        node = _Node(key, value)
        self.cache[key] = node
        self._insert_at_right(node)

        if len(self.cache) > self.capacity:
            least_recent = self.left.next
            if least_recent is not None and least_recent is not self.right:
                self._remove(least_recent)
                del self.cache[least_recent.key]


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))
    cache.put(3, 3)
    print(cache.get(2))
