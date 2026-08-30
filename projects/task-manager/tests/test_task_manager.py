import importlib.util
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]
TASK_MANAGER_DIR = PROJECT_ROOT / "projects" / "task-manager"

authorization_path = TASK_MANAGER_DIR / "authorization.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_authorization",
    authorization_path,
)

module = importlib.util.module_from_spec(spec)

assert spec is not None
assert spec.loader is not None

spec.loader.exec_module(module)

create_task = module.create_task
read_task = module.read_task


@pytest.fixture
def user():
    return {
        "user_id": 2,
        "username": "bob",
        "role": "user",
    }


def test_create_task_for_user(user):
    result = create_task(user, "Write tests")

    assert result["message"] == "Task created"
    assert result["created_by"] == 2
    assert result["title"] == "Write tests"


def test_read_task_for_own_task(user):
    task = {
        "task_id": 101,
        "user_id": 2,
        "title": "Build API",
    }

    result = read_task(user, task)

    assert result == task


def test_read_task_for_another_user_is_forbidden(user):
    task = {
        "task_id": 202,
        "user_id": 3,
        "title": "Someone else's task",
    }

    result = read_task(user, task)

    assert result[1] == 403
    assert result[0]["error"]["code"] == "TASK_ACCESS_FORBIDDEN"
    assert "not allowed" in result[0]["error"]["message"].lower()