"""
Day 62 — Expense Tracker LLD

A small domain model showing Factory + Strategy composition while keeping the
Expense Tracker application service independent from concrete report types.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Expense:
    expense_id: int
    category: str
    amount: float


class ExpenseReportStrategy(Protocol):
    def generate(self, expenses: list[Expense]) -> dict[str, float]:
        ...


class CategoryReportStrategy:
    def generate(self, expenses: list[Expense]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for expense in expenses:
            totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
        return totals


class TotalReportStrategy:
    def generate(self, expenses: list[Expense]) -> dict[str, float]:
        return {"total": sum(expense.amount for expense in expenses)}


class ExpenseReportFactory:
    """Creates report strategies at the composition boundary."""

    _strategies: dict[str, type[ExpenseReportStrategy]] = {
        "category": CategoryReportStrategy,
        "total": TotalReportStrategy,
    }

    @classmethod
    def create(cls, report_type: str) -> ExpenseReportStrategy:
        try:
            return cls._strategies[report_type]()
        except KeyError as exc:
            raise ValueError(f"Unsupported report type: {report_type}") from exc


class ExpenseReportService:
    """Coordinates reporting without depending on a concrete strategy."""

    def __init__(self, factory: type[ExpenseReportFactory] = ExpenseReportFactory) -> None:
        self._factory = factory

    def generate(self, report_type: str, expenses: list[Expense]) -> dict[str, float]:
        strategy = self._factory.create(report_type)
        return strategy.generate(expenses)


def main() -> None:
    expenses = [
        Expense(1, "travel", 1200.0),
        Expense(2, "food", 450.0),
        Expense(3, "travel", 800.0),
    ]

    service = ExpenseReportService()
    print(service.generate("category", expenses))
    print(service.generate("total", expenses))


if __name__ == "__main__":
    main()
