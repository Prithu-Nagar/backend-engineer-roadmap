"""
Day 39 — Clean Architecture Boundaries in Python

Shows a lightweight dependency direction for backend code:

    Interface -> Application -> Domain
                       |
                       v
                Infrastructure

The example keeps the domain model independent from persistence details and
injects infrastructure through a protocol at the application boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Expense:
    """Domain entity with no framework or database dependency."""

    category: str
    amount: float


class ExpenseStore(Protocol):
    """Port required by the application use case."""

    def add(self, expense: Expense) -> None:
        ...

    def total(self) -> float:
        ...


class InMemoryExpenseStore:
    """Infrastructure adapter implementing the application port."""

    def __init__(self) -> None:
        self._expenses: list[Expense] = []

    def add(self, expense: Expense) -> None:
        self._expenses.append(expense)

    def total(self) -> float:
        return sum(expense.amount for expense in self._expenses)


class AddExpense:
    """Application use case depending only on the store abstraction."""

    def __init__(self, store: ExpenseStore) -> None:
        self._store = store

    def execute(self, category: str, amount: float) -> Expense:
        if not category.strip():
            raise ValueError("category must not be empty")
        if amount <= 0:
            raise ValueError("amount must be positive")

        expense = Expense(category.strip(), amount)
        self._store.add(expense)
        return expense


if __name__ == "__main__":
    store = InMemoryExpenseStore()
    add_expense = AddExpense(store)

    add_expense.execute("food", 450.0)
    add_expense.execute("travel", 1200.0)
    print(f"Total expenses: {store.total():.2f}")
