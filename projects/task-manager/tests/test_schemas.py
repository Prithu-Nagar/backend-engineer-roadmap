"""Tests for the locked Task Manager API field contract."""

import importlib.util
from pathlib import Path

TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]
SCHEMAS_PATH = TASK_MANAGER_DIR / "schemas.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_schemas",
    SCHEMAS_PATH,
)
assert spec is not None
assert spec.loader is not None

schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


def test_create_schema_keeps_only_contract_fields():
    payload = {
        "title": "Prepare release",
        "description": "Write the release notes",
        "status": "pending",
        "priority": "high",
        "user_id": 99,
        "is_admin": True,
    }

    assert schemas.create_task_schema(payload) == {
        "title": "Prepare release",
        "description": "Write the release notes",
        "status": "pending",
        "priority": "high",
    }


def test_update_schema_uses_the_same_mutable_fields():
    payload = {
        "status": "completed",
        "priority": "low",
        "id": 123,
    }

    assert schemas.update_task_schema(payload) == {
        "status": "completed",
        "priority": "low",
    }


def test_response_schema_excludes_internal_ownership_and_auth_fields():
    task = {
        "id": 7,
        "title": "Review API",
        "description": None,
        "status": "in_progress",
        "priority": "medium",
        "created_at": "created-at",
        "updated_at": "updated-at",
        "user_id": 4,
        "password_hash": "must-not-leak",
    }

    assert schemas.task_response_schema(task) == {
        "id": 7,
        "title": "Review API",
        "description": None,
        "status": "in_progress",
        "priority": "medium",
        "created_at": "created-at",
        "updated_at": "updated-at",
    }



def test_contract_enumerations_and_pagination_limits_are_stable():
    assert schemas.TASK_STATUSES == {
        "pending",
        "in_progress",
        "completed",
    }
    assert schemas.TASK_PRIORITIES == {"low", "medium", "high"}
    assert schemas.TASK_TITLE_MAX_LENGTH == 200
    assert schemas.DEFAULT_PAGE_SIZE == 20
    assert schemas.MAX_PAGE_SIZE == 100
