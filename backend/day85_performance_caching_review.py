"""Day 85 — Backend performance and caching review helpers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CacheEntry(Generic[T]):
    value: T
    expires_at: float


class TTLCache(Generic[T]):
    """Small in-process TTL cache for demonstrations; not shared across workers."""

    def __init__(self, clock: Callable[[], float] = monotonic) -> None:
        self._clock = clock
        self._entries: dict[str, CacheEntry[T]] = {}

    def get(self, key: str) -> T | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if entry.expires_at <= self._clock():
            del self._entries[key]
            return None
        return entry.value

    def set(self, key: str, value: T, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._entries[key] = CacheEntry(value, self._clock() + ttl_seconds)

    def invalidate(self, key: str) -> None:
        self._entries.pop(key, None)


def cache_aside(cache: TTLCache[T], key: str, loader: Callable[[], T], ttl: float) -> T:
    """Return cached value or load, cache, and return the source-of-truth value."""
    cached = cache.get(key)
    if cached is not None:
        return cached
    value = loader()
    cache.set(key, value, ttl)
    return value


def run_smoke_tests() -> None:
    now = [100.0]
    cache: TTLCache[str] = TTLCache(clock=lambda: now[0])
    cache.set("user:1", "Ada", 5)
    assert cache.get("user:1") == "Ada"
    now[0] += 5
    assert cache.get("user:1") is None
    calls = [0]

    def load() -> str:
        calls[0] += 1
        return "value"

    assert cache_aside(cache, "k", load, 10) == "value"
    assert cache_aside(cache, "k", load, 10) == "value"
    assert calls[0] == 1
    cache.invalidate("k")
    assert cache.get("k") is None


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 85 backend performance/caching checks passed.")
