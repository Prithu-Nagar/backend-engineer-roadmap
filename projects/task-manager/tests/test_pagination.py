"""Day 17 tests for Task Manager pagination, filtering and sorting."""

import importlib.util
from pathlib import Path


TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]
PAGINATION_PATH = TASK_MANAGER_DIR / "pagination.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_pagination",
    PAGINATION_PATH,
)

assert spec is not None
assert spec.loader is not None

pagination = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pagination)


TASKS = [
    {
        "id": 1,
        "title": "Task 1",
        "completed": False,
        "priority": 2,
    },
    {
        "id": 2,
        "title": "Task 2",
        "completed": True,
        "priority": 5,
    },
    {
        "id": 3,
        "title": "Task 3",
        "completed": False,
        "priority": 4,
    },
    {
        "id": 4,
        "title": "Task 4",
        "completed": False,
        "priority": 1,
    },
]


def test_parse_pagination_defaults_and_limits():
    assert pagination.parse_pagination(None, None) == (1, 10)
    assert pagination.parse_pagination("0", "200") == (1, 100)


def test_filter_completed_tasks():
    result = pagination.filter_tasks(TASKS, completed=True)

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_sort_tasks_descending():
    result, error = pagination.sort_tasks(
        TASKS,
        sort_by="priority",
        sort_order="desc",
    )

    assert error is None
    assert [task["id"] for task in result] == [2, 3, 1, 4]


def test_rejects_unknown_sort_field():
    result, error = pagination.sort_tasks(
        TASKS,
        sort_by="unknown",
    )

    assert result is None
    assert "Unsupported sort field" in error


def test_paginate_tasks_returns_correct_page():
    result = pagination.paginate_tasks(
        TASKS,
        page="2",
        per_page="2",
    )

    assert [task["id"] for task in result["tasks"]] == [3, 4]
    assert result["pagination"]["total"] == 4
    assert result["pagination"]["has_previous"] is True
    assert result["pagination"]["has_next"] is False


def test_filter_sort_and_paginate_together():
    result = pagination.paginate_tasks(
        TASKS,
        page="1",
        per_page="2",
        completed=False,
        sort_by="priority",
        sort_order="desc",
    )

    assert [task["id"] for task in result["tasks"]] == [3, 1]
    assert result["pagination"]["total"] == 3