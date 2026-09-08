"""
Day 39 — Expense Tracker Architecture Refactor

Refactors the project around explicit domain, service, and repository
boundaries. The service depends on a repository protocol so persistence can be
changed without moving validation and application rules into the API layer.
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
    def get(self, expense_id: int) -> Expense | None:
        ...

    def save(self, expense: Expense) -> Expense:
        ...


class InMemoryExpenseRepository:
    """Repository adapter used to demonstrate the architecture locally."""

    def __init__(self) -> None:
        self._items: dict[int, Expense] = {}

    def get(self, expense_id: int) -> Expense | None:
        return self._items.get(expense_id)

    def save(self, expense: Expense) -> Expense:
        self._items[expense.expense_id] = expense
        return expense


class ExpenseService:
    """Application rules live here instead of inside transport code."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self._repository = repository

    def add_expense(self, expense_id: int, category: str, amount: float) -> Expense:
        if expense_id <= 0:
            raise ValueError("expense_id must be positive")
        if amount <= 0:
            raise ValueError("amount must be positive")
        category = category.strip()
        if not category:
            raise ValueError("category must not be empty")

        return self._repository.save(Expense(expense_id, category, amount))

    def get_expense(self, expense_id: int) -> Expense | None:
        return self._repository.get(expense_id)


if __name__ == "__main__":
    repository = InMemoryExpenseRepository()
    service = ExpenseService(repository)

    expense = service.add_expense(1, "travel", 2500.0)
    print(expense)
    print(service.get_expense(1))
