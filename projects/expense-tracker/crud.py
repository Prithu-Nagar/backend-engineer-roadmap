"""
Day 32 — Expense Tracker CRUD

A small SQLAlchemy 2.x CRUD layer for the Expense Tracker schema.
The functions receive a Session so transaction ownership remains explicit at
the service/request boundary.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


def create_expense(
    session: Session,
    *,
    amount: Decimal,
    category: str,
    description: str | None,
    expense_date: date,
) -> Expense:
    """Create an expense and flush it into the current transaction."""
    expense = Expense(
        amount=amount,
        category=category,
        description=description,
        expense_date=expense_date,
    )
    session.add(expense)
    session.flush()
    return expense


def get_expense(session: Session, expense_id: int) -> Expense | None:
    """Return one expense by primary key."""
    return session.get(Expense, expense_id)


def list_expenses(
    session: Session,
    *,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Expense]:
    """Return filtered expenses with stable pagination."""
    statement = select(Expense)

    if category is not None:
        statement = statement.where(Expense.category == category)
    if start_date is not None:
        statement = statement.where(Expense.expense_date >= start_date)
    if end_date is not None:
        statement = statement.where(Expense.expense_date <= end_date)

    statement = (
        statement.order_by(Expense.expense_date.desc(), Expense.id.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(session.scalars(statement))


def update_expense(
    session: Session,
    expense_id: int,
    *,
    amount: Decimal | None = None,
    category: str | None = None,
    description: str | None = None,
    expense_date: date | None = None,
) -> Expense | None:
    """Update supported fields and flush the current transaction."""
    expense = session.get(Expense, expense_id)
    if expense is None:
        return None

    if amount is not None:
        expense.amount = amount
    if category is not None:
        expense.category = category
    if description is not None:
        expense.description = description
    if expense_date is not None:
        expense.expense_date = expense_date

    session.flush()
    return expense


def delete_expense(session: Session, expense_id: int) -> bool:
    """Delete an expense and report whether a row was found."""
    expense = session.get(Expense, expense_id)
    if expense is None:
        return False

    session.delete(expense)
    session.flush()
    return True
