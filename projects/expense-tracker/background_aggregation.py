"""
Day 33 — Expense Tracker Background Aggregation

Provides a small SQLAlchemy aggregation function that can be invoked by a
background worker instead of running the aggregation in an HTTP request.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from crud import Expense
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def aggregate_by_category(
    session: Session,
    *,
    owner_id: int,
    start_date: date,
    end_date: date,
) -> list[tuple[str, Decimal]]:
    """Return one owner's category totals for an inclusive date range."""
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")
    statement = (
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.owner_id == owner_id)
        .where(Expense.expense_date >= start_date)
        .where(Expense.expense_date <= end_date)
        .group_by(Expense.category)
        .order_by(Expense.category)
    )

    return [(category, total) for category, total in session.execute(statement)]
