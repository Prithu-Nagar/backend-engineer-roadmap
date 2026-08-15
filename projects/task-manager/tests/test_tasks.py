"""
Task Manager task-operation tests.

Day 15 focus:
- pytest
- fixtures
- assertions
- task authorization
- ownership checks
- CRUD-style task operations
"""

import importlib.util
from pathlib import Path


TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]
AUTHORIZATION_PATH = TASK_MANAGER_DIR / "authorization.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_authorization",
    AUTHORIZATION_PATH,
)

assert spec is not None
assert spec.loader is not None

authorization = importlib.util.module_from_spec(spec)
spec.loader.exec_module(authorization)


def test_create_task(user_data):
    """A regular user can create a task."""

    result = authorization.create_task(
        user_data,
        "Implement testing",
    )

    assert result["message"] == "Task created"
    assert result["created_by"] == user_data["user_id"]
    assert result["title"] == "Implement testing"


def test_read_own_task(user_data, task_data):
    """A user can read their own task."""

    result = authorization.read_task(
        user_data,
        task_data,
    )

    assert result == task_data


def test_cannot_read_another_users_task(
    user_data,
    other_user_task,
):
    """A user cannot read another user's task."""

    result = authorization.read_task(
        user_data,
        other_user_task,
    )

    assert result[1] == 403
    assert "not allowed" in result[0]["error"].lower()


def test_update_own_task(user_data, task_data):
    """A user can update their own task."""

    result = authorization.update_task(
        user_data,
        task_data,
        "Updated task title",
    )

    assert result["title"] == "Updated task title"


def test_cannot_update_another_users_task(
    user_data,
    other_user_task,
):
    """A user cannot update another user's task."""

    result = authorization.update_task(
        user_data,
        other_user_task,
        "Unauthorized update",
    )

    assert result[1] == 403


def test_delete_own_task(user_data, task_data):
    """A user can delete their own task."""

    result = authorization.delete_task(
        user_data,
        task_data,
    )

    assert result["message"] == "Task deleted"
    assert result["task_id"] == task_data["task_id"]


def test_cannot_delete_another_users_task(
    user_data,
    other_user_task,
):
    """A user cannot delete another user's task."""

    result = authorization.delete_task(
        user_data,
        other_user_task,
    )

    assert result[1] == 403


def test_admin_can_access_any_task(
    admin_data,
    other_user_task,
):
    """Admins can access tasks owned by other users."""

    result = authorization.read_task(
        admin_data,
        other_user_task,
    )

    assert result == other_user_task


def test_admin_can_delete_any_task(
    admin_data,
    other_user_task,
):
    """Admins can delete tasks owned by other users."""

    result = authorization.delete_task(
        admin_data,
        other_user_task,
    )

    assert result["message"] == "Task deleted"


def test_multiple_tasks_fixture(multiple_tasks):
    """Verify reusable task fixtures work correctly."""

    assert len(multiple_tasks) == 3

    in_progress = [
        task
        for task in multiple_tasks
        if task["status"] == "in_progress"
    ]

    assert len(in_progress) == 1
    assert in_progress[0]["task_id"] == 2