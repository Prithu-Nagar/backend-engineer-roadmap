"""
Day 62 — Factory and Strategy Design Patterns in Python

A backend-oriented example showing how a factory can select a strategy while
keeping the application service independent from concrete implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Expense:
    expense_id: int
    category: str
    amount: float


class ReportStrategy(Protocol):
    """Contract for interchangeable expense-report calculations."""

    def build(self, expenses: list[Expense]) -> dict[str, float]:
        ...


class CategorySummaryStrategy:
    def build(self, expenses: list[Expense]) -> dict[str, float]:
        summary: dict[str, float] = {}
        for expense in expenses:
            summary[expense.category] = summary.get(expense.category, 0.0) + expense.amount
        return summary


class TotalSummaryStrategy:
    def build(self, expenses: list[Expense]) -> dict[str, float]:
        return {"total": sum(expense.amount for expense in expenses)}


class ReportStrategyFactory:
    """Factory that selects a report strategy from an explicit report type."""

    _strategies: dict[str, type[ReportStrategy]] = {
        "category": CategorySummaryStrategy,
        "total": TotalSummaryStrategy,
    }

    @classmethod
    def create(cls, report_type: str) -> ReportStrategy:
        try:
            strategy_type = cls._strategies[report_type]
        except KeyError as exc:
            raise ValueError(f"Unsupported report type: {report_type}") from exc
        return strategy_type()


class ExpenseReportService:
    """Application service using a strategy without knowing its implementation."""

    def __init__(
        self, strategy_factory: type[ReportStrategyFactory] = ReportStrategyFactory
    ) -> None:
        self._strategy_factory = strategy_factory

    def build_report(self, report_type: str, expenses: list[Expense]) -> dict[str, float]:
        if not expenses:
            return {}
        strategy = self._strategy_factory.create(report_type)
        return strategy.build(expenses)


def main() -> None:
    expenses = [
        Expense(1, "travel", 1200.0),
        Expense(2, "food", 450.0),
        Expense(3, "travel", 800.0),
    ]

    service = ExpenseReportService()
    print(service.build_report("category", expenses))
    print(service.build_report("total", expenses))


if __name__ == "__main__":
    main()
