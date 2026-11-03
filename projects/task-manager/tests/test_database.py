"""Integration checks for the Task Manager database foundation."""

import pytest
from sqlalchemy import delete, inspect, text
from sqlalchemy.exc import IntegrityError

from backend.app import create_app
from backend.config import TestingConfig
from backend.extensions import db
from backend.models import Task, User


@pytest.fixture
def app():
    application = create_app(TestingConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


def test_test_configuration_uses_isolated_in_memory_database(app):
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_clean_database_initialization_creates_expected_tables(app):
    inspector = inspect(db.engine)
    assert set(inspector.get_table_names()) == {"users", "tasks"}


def test_migration_initializes_a_clean_database():
    application = create_app(TestingConfig)
    result = application.test_cli_runner().invoke(args=["db", "upgrade"])

    assert result.exit_code == 0, result.output

    with application.app_context():
        try:
            inspector = inspect(db.engine)
            assert set(inspector.get_table_names()) == {
                "alembic_version",
                "tasks",
                "users",
            }
            assert {
                index["name"] for index in inspector.get_indexes("tasks")
            } == {
                "idx_tasks_created_at",
                "idx_tasks_user_id",
                "idx_tasks_user_priority",
                "idx_tasks_user_status",
            }
            assert any(
                foreign_key["name"] == "tasks_user_fk"
                for foreign_key in inspector.get_foreign_keys("tasks")
            )
            assert db.session.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one() == "0001_create_users_tasks"
        finally:
            db.session.remove()
            db.engine.dispose()


def test_user_and_task_relationship_persists(app):
    user = User(
        username="  task-owner  ",
        email="OWNER@EXAMPLE.COM",
        password_hash="hashed",
    )
    task = Task(title="  Build database layer  ", description="MVP persistence")
    user.tasks.append(task)
    db.session.add(user)
    db.session.commit()

    saved_task = db.session.get(Task, task.id)
    assert saved_task is not None
    assert saved_task.title == "Build database layer"
    assert saved_task.user_id == user.id
    assert saved_task.owner.email == "owner@example.com"
    assert saved_task.status == "pending"
    assert saved_task.priority == "medium"


def test_unique_user_identity_is_enforced_by_database(app):
    db.session.add(
        User(username="same", email="same@example.com", password_hash="hash")
    )
    db.session.commit()
    db.session.add(
        User(username="same", email="other@example.com", password_hash="hash")
    )

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_task_model_rejects_invalid_status(app):
    with pytest.raises(ValueError, match="status is not supported"):
        Task(title="Invalid status", status="blocked")


def test_database_health_endpoint_uses_configured_database(client):
    response = client.get("/health/database")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "database": "connected"}



def test_database_enforces_owner_cascade_delete(app):
    user = User(username="cascade", email="cascade@example.com", password_hash="hash")
    user.tasks.append(Task(title="Delete with owner"))
    db.session.add(user)
    db.session.commit()
    task_id = user.tasks[0].id

    db.session.execute(delete(User).where(User.id == user.id))
    db.session.commit()

    assert db.session.get(Task, task_id) is None
