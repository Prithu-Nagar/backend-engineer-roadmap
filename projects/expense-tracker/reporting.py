"""
Owner-scoped expense summaries and monthly budget progress.

All monetary calculations use Decimal values returned by SQL NUMERIC columns.
The caller owns the SQLAlchemy Session and its transaction lifecycle.
"""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from crud import Budget, Expense
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def _validate_range(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")


def summarize_expenses(
    session: Session,
    *,
    owner_id: int,
    start_date: date,
    end_date: date,
    category: str | None = None,
) -> dict[str, object]:
    """Return owner-scoped totals and stable per-category aggregates."""
    _validate_range(start_date, end_date)
    filters = [
        Expense.owner_id == owner_id,
        Expense.expense_date >= start_date,
        Expense.expense_date <= end_date,
    ]
    if category is not None:
        filters.append(Expense.category == category)

    total, count = session.execute(
        select(func.coalesce(func.sum(Expense.amount), 0), func.count(Expense.id))
        .where(*filters)
    ).one()

    rows = session.execute(
        select(Expense.category, func.sum(Expense.amount), func.count(Expense.id))
        .where(*filters)
        .group_by(Expense.category)
        .order_by(Expense.category)
    ).all()

    return {
        "total": Decimal(total),
        "expense_count": int(count),
        "by_category": [
            {
                "category": name,
                "total": Decimal(amount),
                "expense_count": int(category_count),
            }
            for name, amount, category_count in rows
        ],
        "start_date": start_date,
        "end_date": end_date,
    }


def monthly_budget_progress(
    session: Session,
    *,
    owner_id: int,
    month_start: date,
) -> list[dict[str, object]]:
    """Compare each category budget with that owner's month-to-date spending."""
    if month_start.day != 1:
        raise ValueError("month_start must be the first day of a month")

    if month_start.month == 12:
        next_month = date(month_start.year + 1, 1, 1)
    else:
        next_month = date(month_start.year, month_start.month + 1, 1)

    budgets = session.scalars(
        select(Budget)
        .where(
            Budget.owner_id == owner_id,
            Budget.month_start == month_start,
        )
        .order_by(Budget.category, Budget.id)
    ).all()

    spend_rows = session.execute(
        select(Expense.category, func.coalesce(func.sum(Expense.amount), 0))
        .where(
            Expense.owner_id == owner_id,
            Expense.expense_date >= month_start,
            Expense.expense_date < next_month,
        )
        .group_by(Expense.category)
    ).all()
    spent_by_category = {name: Decimal(amount) for name, amount in spend_rows}

    results = []
    for budget in budgets:
        spent = spent_by_category.get(budget.category, Decimal("0.00"))
        remaining = budget.amount - spent
        percentage = (
            (spent / budget.amount * Decimal(100)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        )
        results.append(
            {
                "budget_id": budget.id,
                "category": budget.category,
                "budget": Decimal(budget.amount),
                "spent": spent,
                "remaining": remaining,
                "percentage_used": percentage,
                "over_budget": spent > budget.amount,
            }
        )
    return results
