"""
Day 33 — Expense Tracker Background Aggregation

Provides a small SQLAlchemy aggregation function that can be invoked by a
background worker instead of running the aggregation in an HTTP request.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from crud import Expense


def aggregate_by_category(
    session: Session,
    *,
    start_date: date,
    end_date: date,
) -> list[tuple[str, Decimal]]:
    """Return total expense amount grouped by category for a date range."""
    statement = (
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.expense_date >= start_date)
        .where(Expense.expense_date <= end_date)
        .group_by(Expense.category)
        .order_by(Expense.category)
    )

    return [(category, total) for category, total in session.execute(statement)]
