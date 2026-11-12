import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from background_aggregation import aggregate_by_category
from crud import (
    Base,
    create_budget,
    create_expense,
    delete_budget,
    get_budget,
    list_budgets,
    update_budget,
)
from reporting import monthly_budget_progress, summarize_expenses
from test_crud import User


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as db:
        db.add_all([User(id=1, username="alice"), User(id=2, username="bob")])
        db.commit()
        yield db
        db.rollback()
    engine.dispose()


def add_expense(db, owner_id, category, amount, when):
    return create_expense(
        db,
        owner_id=owner_id,
        amount=Decimal(amount),
        category=category,
        description=None,
        expense_date=when,
    )


def test_summary_filters_owner_and_inclusive_dates(session):
    add_expense(session, 1, "Food", "10.25", date(2025, 1, 1))
    add_expense(session, 1, "Food", "4.75", date(2025, 1, 31))
    add_expense(session, 1, "Travel", "20.00", date(2025, 2, 1))
    add_expense(session, 2, "Food", "999.00", date(2025, 1, 15))
    session.flush()

    result = summarize_expenses(
        session,
        owner_id=1,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    assert result["total"] == Decimal("15.00")
    assert result["expense_count"] == 2
    assert result["by_category"] == [
        {"category": "Food", "total": Decimal("15.00"), "expense_count": 2}
    ]


def test_summary_category_filter_and_empty_result(session):
    add_expense(session, 1, "Food", "10.00", date(2025, 1, 5))
    session.flush()

    result = summarize_expenses(
        session,
        owner_id=1,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
        category="Travel",
    )
    assert result["total"] == Decimal(0)
    assert result["expense_count"] == 0
    assert result["by_category"] == []


def test_summary_rejects_reversed_date_range(session):
    with pytest.raises(ValueError, match="start_date"):
        summarize_expenses(
            session,
            owner_id=1,
            start_date=date(2025, 2, 1),
            end_date=date(2025, 1, 1),
        )


def test_monthly_budget_progress_and_owner_isolation(session):
    create_budget(
        session, owner_id=1, category="Food",
        month_start=date(2025, 1, 1), amount=Decimal("100.00")
    )
    create_budget(
        session, owner_id=1, category="Travel",
        month_start=date(2025, 1, 1), amount=Decimal("50.00")
    )
    create_budget(
        session, owner_id=2, category="Food",
        month_start=date(2025, 1, 1), amount=Decimal("500.00")
    )
    add_expense(session, 1, "Food", "125.00", date(2025, 1, 15))
    add_expense(session, 2, "Food", "20.00", date(2025, 1, 15))
    session.flush()

    progress = monthly_budget_progress(
        session, owner_id=1, month_start=date(2025, 1, 1)
    )
    assert [row["category"] for row in progress] == ["Food", "Travel"]
    assert progress[0]["spent"] == Decimal("125.00")
    assert progress[0]["remaining"] == Decimal("-25.00")
    assert progress[0]["percentage_used"] == Decimal("125.00")
    assert progress[0]["over_budget"] is True
    assert progress[1]["spent"] == Decimal("0.00")
    assert progress[1]["over_budget"] is False


def test_budget_crud_is_owner_scoped_and_transaction_owned(session):
    budget = create_budget(
        session, owner_id=1, category="Food",
        month_start=date(2025, 1, 1), amount=Decimal("100.00")
    )
    session.flush()

    assert get_budget(session, budget.id, owner_id=2) is None
    assert len(list_budgets(session, owner_id=2)) == 0
    assert update_budget(
        session, budget.id, owner_id=2, amount=Decimal("200.00")
    ) is None
    assert update_budget(
        session, budget.id, owner_id=1, amount=Decimal("150.00")
    ).amount == Decimal("150.00")
    assert delete_budget(session, budget.id, owner_id=2) is False
    assert delete_budget(session, budget.id, owner_id=1) is True


def test_budget_month_and_owner_category_month_are_constrained(session):
    create_budget(
        session, owner_id=1, category="Food",
        month_start=date(2025, 1, 1), amount=Decimal("100.00")
    )
    session.flush()
    with pytest.raises(IntegrityError):
        create_budget(
            session, owner_id=1, category="Food",
            month_start=date(2025, 1, 1), amount=Decimal("120.00")
        )
    session.rollback()

    with pytest.raises(ValueError, match="first day"):
        create_budget(
            session, owner_id=1, category="Food",
            month_start=date(2025, 1, 2), amount=Decimal("100.00")
        )


def test_background_aggregation_is_owner_scoped(session):
    add_expense(session, 1, "Food", "10.00", date(2025, 1, 5))
    add_expense(session, 2, "Food", "900.00", date(2025, 1, 5))
    add_expense(session, 1, "Travel", "5.00", date(2025, 1, 6))
    session.flush()

    assert aggregate_by_category(
        session,
        owner_id=1,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    ) == [("Food", Decimal("10.00")), ("Travel", Decimal("5.00"))]
