"""Run a persistent local demonstration of Expense Tracker aggregation.

The demo uses SQLite for a self-contained local run. The worker is in-process
and intentionally does not claim durable queue delivery.
"""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, date, datetime
from decimal import Decimal

from async_processing import (
    AggregationJob,
    AsyncAggregationWorker,
    create_aggregation_handler,
)
from crud import Base, Expense, create_expense
from sqlalchemy import String, create_engine, func, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker


class User(Base):
    """Minimal user table required by the Expense Tracker foreign keys."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)


async def run_worker(session_factory: sessionmaker) -> list[tuple[str, Decimal]]:
    """Run one persisted aggregation through the in-process worker."""
    worker = AsyncAggregationWorker(create_aggregation_handler(session_factory))
    await worker.start()
    try:
        result_future = await worker.submit(
            AggregationJob(
                owner_id=1,
                start_date=date.min,
                end_date=datetime.now(UTC).date(),
            )
        )
        return await result_future
    finally:
        await worker.stop()


def main() -> None:
    """Initialize the local database, seed one example, and run aggregation."""
    database_url = os.getenv("DATABASE_URL", "sqlite:///expense-tracker.db")
    url = make_url(database_url)
    connect_args = (
        {"check_same_thread": False}
        if url.get_backend_name() == "sqlite"
        else {}
    )
    engine = create_engine(database_url, connect_args=connect_args)
    try:
        Base.metadata.create_all(engine)
        factory = sessionmaker(bind=engine, expire_on_commit=False)

        with factory.begin() as session:
            if session.get(User, 1) is None:
                session.add(User(id=1, username="demo-owner"))
                session.flush()

            existing = session.scalar(
                select(func.count())
                .select_from(Expense)
                .where(Expense.owner_id == 1)
            )
            if not existing:
                create_expense(
                    session,
                    owner_id=1,
                    amount=Decimal("24.50"),
                    category="Demo",
                    description="Sample expense for the local worker demo",
                    expense_date=datetime.now(UTC).date(),
                )

        totals = asyncio.run(run_worker(factory))
        print("Expense Tracker category totals:")
        for category, amount in totals:
            print(f"- {category}: {amount:.2f}")
        if not totals:
            print("- No expenses found for the demo owner")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
