"""
Day 35 — Application-Level Caching

Demonstrates a small cache-aside implementation with TTL expiration.
Production services normally use a shared cache such as Redis when multiple
application instances need a common cache.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class CacheEntry(Generic[T]):
    value: T
    expires_at: float


class TTLCache(Generic[T]):
    """Small in-process cache with time-based expiration."""

    def __init__(self, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._ttl = ttl_seconds
        self._entries: dict[str, CacheEntry[T]] = {}

    def get(self, key: str) -> T | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if time.monotonic() >= entry.expires_at:
            self._entries.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: T) -> None:
        self._entries[key] = CacheEntry(value, time.monotonic() + self._ttl)

    def invalidate(self, key: str) -> None:
        self._entries.pop(key, None)


def cache_aside(
    cache: TTLCache[T], key: str, loader: Callable[[], T]
) -> T:
    """Return a cached value or load and populate the cache on a miss."""
    cached = cache.get(key)
    if cached is not None:
        return cached

    value = loader()
    cache.set(key, value)
    return value


if __name__ == "__main__":
    cache = TTLCache[str](ttl_seconds=10)
    print(cache_aside(cache, "expense:1001", lambda: "loaded from database"))
    print(cache_aside(cache, "expense:1001", lambda: "should not run on a hit"))
