"""
Day 36 — Expense Tracker Redis Caching

Adds a Redis-backed cache adapter around the existing Expense Tracker cache
contract. The service remains responsible for cache-aside reads and explicit
invalidation, while Redis provides a shared cache across application instances.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Protocol

import redis

from caching_layer import Expense, ExpenseRepository


class ExpenseCache(Protocol):
    def get(self, key: str) -> str | None:
        ...

    def set(self, key: str, value: str, ex: int) -> None:
        ...

    def delete(self, key: str) -> None:
        ...


class RedisExpenseCache:
    """Serialize Expense values into a Redis cache."""

    def __init__(
        self,
        client: redis.Redis,
        ttl_seconds: int = 300,
        prefix: str = "expense:",
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._client = client
        self._ttl_seconds = ttl_seconds
        self._prefix = prefix

    def get(self, key: str) -> Expense | None:
        payload = self._client.get(self._prefix + key)
        if payload is None:
            return None

        data = json.loads(payload)
        return Expense(
            expense_id=int(data["expense_id"]),
            category=str(data["category"]),
            amount=float(data["amount"]),
        )

    def set(self, key: str, value: Expense) -> None:
        payload = json.dumps(asdict(value))
        self._client.set(self._prefix + key, payload, ex=self._ttl_seconds)

    def invalidate(self, key: str) -> None:
        self._client.delete(self._prefix + key)


class CachedExpenseRepository:
    """Apply cache-aside reads around the source repository."""

    def __init__(
        self,
        repository: ExpenseRepository,
        cache: RedisExpenseCache,
    ) -> None:
        self._repository = repository
        self._cache = cache

    def get_by_id(self, expense_id: int) -> Expense | None:
        key = str(expense_id)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        expense = self._repository.get_by_id(expense_id)
        if expense is not None:
            self._cache.set(key, expense)
        return expense

    def invalidate(self, expense_id: int) -> None:
        self._cache.invalidate(str(expense_id))


def build_redis_cache(
    url: str = "redis://localhost:6379/0",
    ttl_seconds: int = 300,
) -> RedisExpenseCache:
    """Create the Redis cache used by the Expense Tracker."""
    client: redis.Redis = redis.Redis.from_url(
        url,
        decode_responses=True,
    )
    return RedisExpenseCache(client, ttl_seconds=ttl_seconds)
