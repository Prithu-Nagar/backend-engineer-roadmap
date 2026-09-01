"""
Day 32 — SQLAlchemy ORM Session Concepts

A small SQLAlchemy 2.x example covering:
- Declarative ORM models
- Session lifecycle
- Commit and rollback
- Querying through a Session
- Keeping transaction boundaries explicit
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, create_engine, select
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


def create_engine_with_schema(database_url: str = "sqlite:///sqlalchemy_demo.db"):
    """Create an engine and return a session factory."""
    engine = create_engine(database_url, future=True)
    Base.metadata.create_all(engine)
    return engine


def add_expense(session: Session) -> Expense:
    """Add an expense and commit the transaction."""
    expense = Expense(
        amount=Decimal("125.50"),
        category="food",
        description="Team lunch",
        expense_date=date.today(),
    )
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


def list_expenses(session: Session) -> list[Expense]:
    """Query expenses through the current Session."""
    return list(session.scalars(select(Expense).order_by(Expense.id)))


def demonstrate_rollback(session: Session) -> None:
    """Show that a failed unit of work should be rolled back."""
    try:
        session.add(
            Expense(
                amount=Decimal("20.00"),
                category="invalid-example",
                description="Demonstration",
                expense_date=date.today(),
            )
        )
        raise RuntimeError("simulate application failure")
    except RuntimeError:
        session.rollback()


if __name__ == "__main__":
    engine = create_engine_with_schema()

    with Session(engine) as session:
        expense = add_expense(session)
        print(f"Created expense: {expense.id}")

        demonstrate_rollback(session)

        for item in list_expenses(session):
            print(item.id, item.amount, item.category)
