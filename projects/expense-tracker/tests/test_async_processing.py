import asyncio
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from async_processing import (
    AggregationJob,
    AsyncAggregationWorker,
    create_aggregation_handler,
)
from crud import Base, create_expense
from test_crud import User


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as session:
        session.add_all(
            [User(id=1, username="alice"), User(id=2, username="bob")]
        )
        session.flush()
        session.add_all(
            [
                create_expense(
                    session,
                    owner_id=1,
                    amount=Decimal("10.25"),
                    category="Food",
                    description=None,
                    expense_date=date(2025, 1, 5),
                ),
                create_expense(
                    session,
                    owner_id=2,
                    amount=Decimal("999.00"),
                    category="Food",
                    description=None,
                    expense_date=date(2025, 1, 5),
                ),
            ]
        )
        session.commit()
    yield factory
    engine.dispose()


def test_worker_returns_owner_scoped_persistent_aggregation(session_factory):
    async def run_job():
        worker = AsyncAggregationWorker(
            create_aggregation_handler(session_factory)
        )
        await worker.start()
        try:
            result = await worker.submit(
                AggregationJob(
                    owner_id=1,
                    start_date=date(2025, 1, 1),
                    end_date=date(2025, 1, 31),
                )
            )
            await worker.wait_for_completion()
            return await result
        finally:
            await worker.stop()

    assert asyncio.run(run_job()) == [("Food", Decimal("10.25"))]


def test_job_failure_is_returned_and_worker_continues(session_factory):
    async def run_jobs():
        worker = AsyncAggregationWorker(
            create_aggregation_handler(session_factory)
        )
        await worker.start()
        try:
            failed = await worker.submit(
                AggregationJob(
                    owner_id=1,
                    start_date=date(2025, 2, 1),
                    end_date=date(2025, 1, 1),
                )
            )
            succeeded = await worker.submit(
                AggregationJob(
                    owner_id=1,
                    start_date=date(2025, 1, 1),
                    end_date=date(2025, 1, 31),
                )
            )
            await worker.wait_for_completion()
            with pytest.raises(ValueError, match="start_date"):
                await failed
            assert await succeeded == [("Food", Decimal("10.25"))]
        finally:
            await worker.stop()

    asyncio.run(run_jobs())
