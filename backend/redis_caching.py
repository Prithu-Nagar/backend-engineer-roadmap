"""
Day 36 — Redis Caching Patterns

Demonstrates cache-aside behavior with Redis while keeping cache access behind
a small interface. The Redis client is created outside the service so the
application can manage connection configuration and lifecycle.
"""

from __future__ import annotations

import json
from typing import Protocol

import redis


class Cache(Protocol):
    def get(self, key: str) -> str | None:
        ...

    def set(self, key: str, value: str, ex: int) -> None:
        ...

    def delete(self, key: str) -> None:
        ...


class RedisCache:
    """Small Redis-backed cache adapter."""

    def __init__(self, client: redis.Redis, prefix: str = "backend:") -> None:
        self._client = client
        self._prefix = prefix

    def get(self, key: str) -> str | None:
        return self._client.get(self._prefix + key)

    def set(self, key: str, value: str, ex: int) -> None:
        self._client.set(self._prefix + key, value, ex=ex)

    def delete(self, key: str) -> None:
        self._client.delete(self._prefix + key)


def cache_aside_json(
    cache: Cache,
    key: str,
    loader,
    ttl_seconds: int = 300,
):
    """Load JSON-serializable data on a miss and cache it with a TTL."""
    cached = cache.get(key)
    if cached is not None:
        return json.loads(cached)

    value = loader()
    cache.set(key, json.dumps(value), ex=ttl_seconds)
    return value


def invalidate(cache: Cache, key: str) -> None:
    """Explicitly invalidate a cache key after a source-of-truth change."""
    cache.delete(key)


def build_redis_cache(url: str = "redis://localhost:6379/0") -> RedisCache:
    """Create a Redis cache adapter from a connection URL."""
    client: redis.Redis = redis.Redis.from_url(
        url,
        decode_responses=True,
    )
    return RedisCache(client)


if __name__ == "__main__":
    cache = build_redis_cache()
    key = "expense:1001"

    # This example expects a Redis server to be available locally.
    value = cache_aside_json(
        cache,
        key,
        lambda: {"expense_id": 1001, "category": "travel", "amount": 2500.0},
        ttl_seconds=60,
    )
    print(value)

    invalidate(cache, key)
