import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from crud import (
    Base,
    create_category,
    create_expense,
    delete_category,
    delete_expense,
    get_category,
    get_expense,
    list_categories,
    list_expenses,
    update_category,
    update_expense,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)


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


def make_expense(session, owner_id=1, category="Food"):
    return create_expense(
        session,
        owner_id=owner_id,
        amount=Decimal("12.50"),
        category=category,
        description="Lunch",
        expense_date=date(2025, 1, 1),
    )


def test_expense_crud_is_scoped_to_owner(session):
    expense = make_expense(session)
    session.commit()

    assert get_expense(session, expense.id, owner_id=1) is expense
    assert get_expense(session, expense.id, owner_id=2) is None
    assert list_expenses(session, owner_id=2) == []

    updated = update_expense(
        session, expense.id, owner_id=2, description="Unauthorized"
    )
    assert updated is None
    assert expense.description == "Lunch"
    assert delete_expense(session, expense.id, owner_id=2) is False

    assert update_expense(
        session, expense.id, owner_id=1, amount=Decimal("14.00")
    ).amount == Decimal("14.00")
    assert delete_expense(session, expense.id, owner_id=1) is True
    assert get_expense(session, expense.id, owner_id=1) is None


def test_expense_list_filters_and_orders_only_owner_rows(session):
    first = make_expense(session, owner_id=1, category="Food")
    second = make_expense(session, owner_id=1, category="Travel")
    make_expense(session, owner_id=2, category="Food")
    session.commit()

    results = list_expenses(session, owner_id=1, category="Food", limit=10)
    assert [item.id for item in results] == [first.id]
    assert second.owner_id == 1
    assert len(list_expenses(session, owner_id=1)) == 2


def test_category_crud_and_owner_isolation(session):
    category = create_category(session, owner_id=1, name="Food")
    session.commit()

    assert get_category(session, category.id, owner_id=1) is category
    assert get_category(session, category.id, owner_id=2) is None
    assert [item.name for item in list_categories(session, owner_id=1)] == ["Food"]
    assert list_categories(session, owner_id=2) == []

    assert update_category(
        session, category.id, owner_id=2, name="Travel"
    ) is None
    assert category.name == "Food"
    assert update_category(
        session, category.id, owner_id=1, name="Dining"
    ).name == "Dining"

    assert delete_category(session, category.id, owner_id=2) is False
    assert delete_category(session, category.id, owner_id=1) is True


def test_category_name_is_unique_per_owner(session):
    create_category(session, owner_id=1, name="Food")
    session.flush()
    create_category(session, owner_id=2, name="Food")
    session.flush()

    with pytest.raises(IntegrityError):
        create_category(session, owner_id=1, name="Food")
    session.rollback()


def test_crud_helpers_leave_commit_and_rollback_to_caller(session):
    expense = make_expense(session)
    expense_id = expense.id
    session.rollback()

    assert get_expense(session, expense_id, owner_id=1) is None



def test_failed_multi_step_transaction_rolls_back_all_writes(session):
    from crud import Budget, create_budget

    with pytest.raises(IntegrityError), session.begin():
        make_expense(session, owner_id=1, category="Food")
        create_budget(
            session,
            owner_id=1,
            category="Food",
            month_start=date(2025, 1, 1),
            amount=Decimal("100.00"),
        )
        create_budget(
            session,
            owner_id=1,
            category="Food",
            month_start=date(2025, 1, 1),
            amount=Decimal("125.00"),
        )

    assert list_expenses(session, owner_id=1) == []
    assert session.query(Budget).count() == 0
