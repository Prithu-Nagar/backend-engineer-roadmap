"""
Day 39 — Service / Repository Layer Patterns

Demonstrates separation between application services and persistence code.
The service depends on a repository protocol instead of a concrete database
implementation, making transaction ownership and testing boundaries explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Expense:
    """Domain object used by the application service."""

    expense_id: int
    category: str
    amount: float


class ExpenseRepository(Protocol):
    """Persistence contract required by the service layer."""

    def get_by_id(self, expense_id: int) -> Expense | None:
        ...

    def save(self, expense: Expense) -> Expense:
        ...


class InMemoryExpenseRepository:
    """Small repository implementation for local examples and tests."""

    def __init__(self) -> None:
        self._items: dict[int, Expense] = {}

    def get_by_id(self, expense_id: int) -> Expense | None:
        return self._items.get(expense_id)

    def save(self, expense: Expense) -> Expense:
        self._items[expense.expense_id] = expense
        return expense


class ExpenseService:
    """Application service that coordinates domain-level operations."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self._repository = repository

    def create_expense(
        self,
        *,
        expense_id: int,
        category: str,
        amount: float,
    ) -> Expense:
        if expense_id <= 0:
            raise ValueError("expense_id must be positive")
        if amount <= 0:
            raise ValueError("amount must be positive")
        if not category.strip():
            raise ValueError("category must not be empty")

        expense = Expense(expense_id, category.strip(), amount)
        return self._repository.save(expense)

    def get_expense(self, expense_id: int) -> Expense | None:
        return self._repository.get_by_id(expense_id)


if __name__ == "__main__":
    repository = InMemoryExpenseRepository()
    service = ExpenseService(repository)

    created = service.create_expense(
        expense_id=1,
        category="travel",
        amount=2500.0,
    )
    print(created)
    print(service.get_expense(1))
