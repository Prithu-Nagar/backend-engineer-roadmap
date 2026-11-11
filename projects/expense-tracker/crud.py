"""
Expense Tracker persistence models and CRUD operations.

CRUD helpers flush changes but never commit or close the caller-owned Session.
The request/service boundary is responsible for committing or rolling back.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    """Declarative base for the Expense Tracker persistence models."""


class Category(Base):
    __tablename__ = "expense_categories"
    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_expense_category_owner_name"),
        CheckConstraint("length(trim(name)) > 0", name="expense_category_name_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        CheckConstraint("amount > 0", name="expenses_amount_check"),
        CheckConstraint("length(trim(category)) > 0", name="expenses_category_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def create_category(session: Session, *, owner_id: int, name: str) -> Category:
    """Create an owner-scoped category in the current transaction."""
    category = Category(owner_id=owner_id, name=name)
    session.add(category)
    session.flush()
    return category


def get_category(
    session: Session, category_id: int, *, owner_id: int
) -> Category | None:
    """Return a category only when it belongs to the supplied owner."""
    statement = select(Category).where(
        Category.id == category_id, Category.owner_id == owner_id
    )
    return session.scalar(statement)


def list_categories(session: Session, *, owner_id: int) -> list[Category]:
    """List categories belonging to one owner."""
    statement = (
        select(Category)
        .where(Category.owner_id == owner_id)
        .order_by(Category.name, Category.id)
    )
    return list(session.scalars(statement))


def update_category(
    session: Session, category_id: int, *, owner_id: int, name: str
) -> Category | None:
    """Rename an owner's category; never update another owner's record."""
    category = get_category(session, category_id, owner_id=owner_id)
    if category is None:
        return None
    category.name = name
    session.flush()
    return category


def delete_category(session: Session, category_id: int, *, owner_id: int) -> bool:
    """Delete an owner's category and report whether it existed."""
    category = get_category(session, category_id, owner_id=owner_id)
    if category is None:
        return False
    session.delete(category)
    session.flush()
    return True


def create_expense(
    session: Session,
    *,
    owner_id: int,
    amount: Decimal,
    category: str,
    description: str | None,
    expense_date: date,
) -> Expense:
    """Create an expense and flush it into the current transaction."""
    expense = Expense(
        owner_id=owner_id,
        amount=amount,
        category=category,
        description=description,
        expense_date=expense_date,
    )
    session.add(expense)
    session.flush()
    return expense


def get_expense(
    session: Session, expense_id: int, *, owner_id: int
) -> Expense | None:
    """Return an expense only when it belongs to the supplied owner."""
    statement = select(Expense).where(
        Expense.id == expense_id, Expense.owner_id == owner_id
    )
    return session.scalar(statement)


def list_expenses(
    session: Session,
    *,
    owner_id: int,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Expense]:
    """Return one owner's expenses with stable pagination."""
    statement = select(Expense).where(Expense.owner_id == owner_id)

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
    owner_id: int,
    amount: Decimal | None = None,
    category: str | None = None,
    description: str | None = None,
    expense_date: date | None = None,
) -> Expense | None:
    """Update supported fields for an expense owned by the caller."""
    expense = get_expense(session, expense_id, owner_id=owner_id)
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


def delete_expense(
    session: Session, expense_id: int, *, owner_id: int
) -> bool:
    """Delete an expense only when it belongs to the supplied owner."""
    expense = get_expense(session, expense_id, owner_id=owner_id)
    if expense is None:
        return False
    session.delete(expense)
    session.flush()
    return True
