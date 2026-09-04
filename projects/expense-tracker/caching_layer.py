"""
Day 35 — Expense Tracker Caching Layer

Adds a small application-side cache boundary around expense lookups. The
cache is deliberately injected so the project can later replace it with Redis
without changing the service's lookup contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Expense:
    expense_id: int
    category: str
    amount: float


class ExpenseRepository(Protocol):
    def get_by_id(self, expense_id: int) -> Expense | None:
        ...


class Cache(Protocol):
    def get(self, key: str) -> Expense | None:
        ...

    def set(self, key: str, value: Expense) -> None:
        ...

    def invalidate(self, key: str) -> None:
        ...


class ExpenseCacheService:
    """Implement cache-aside lookup and explicit invalidation."""

    def __init__(self, repository: ExpenseRepository, cache: Cache) -> None:
        self._repository = repository
        self._cache = cache

    def get_expense(self, expense_id: int) -> Expense | None:
        key = self._key(expense_id)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        expense = self._repository.get_by_id(expense_id)
        if expense is not None:
            self._cache.set(key, expense)
        return expense

    def invalidate_expense(self, expense_id: int) -> None:
        self._cache.invalidate(self._key(expense_id))

    @staticmethod
    def _key(expense_id: int) -> str:
        return f"expense:{expense_id}"
