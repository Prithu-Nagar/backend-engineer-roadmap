"""Day 83 — Small domain service for the capstone implementation sprint.

This in-memory implementation defines behavior and tests without assuming a
specific ORM. Replace TaskRepository with a database-backed adapter for use
in the application.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from threading import Lock
from typing import Any


class TaskValidationError(ValueError):
    """Raised when task input violates the service contract."""


class TaskNotFoundError(LookupError):
    """Raised when a task does not exist."""


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    description: str = ""
    status: str = "todo"


class TaskService:
    """Validate task operations and manage a simple in-memory collection."""

    ALLOWED_FIELDS = frozenset({"title", "description", "status"})
    ALLOWED_STATUSES = frozenset({"todo", "in_progress", "done"})

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._ids = count(1)
        self._lock = Lock()

    def create(self, payload: dict[str, Any]) -> Task:
        if not isinstance(payload, dict):
            raise TaskValidationError("payload must be an object")
        unknown = set(payload) - self.ALLOWED_FIELDS
        if unknown:
            raise TaskValidationError(
                f"unsupported fields: {', '.join(sorted(unknown))}"
            )
        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError("title must be a non-empty string")
        description = payload.get("description", "")
        if not isinstance(description, str):
            raise TaskValidationError("description must be a string")
        status = payload.get("status", "todo")
        if status not in self.ALLOWED_STATUSES:
            raise TaskValidationError("status is not supported")

        with self._lock:
            task = Task(next(self._ids), title.strip(), description, status)
            self._tasks[task.task_id] = task
            return task

    def get(self, task_id: int) -> Task:
        with self._lock:
            try:
                return self._tasks[task_id]
            except KeyError as exc:
                raise TaskNotFoundError(f"task {task_id} was not found") from exc

    def update(self, task_id: int, changes: dict[str, Any]) -> Task:
        if not isinstance(changes, dict) or not changes:
            raise TaskValidationError("changes must be a non-empty object")
        unknown = set(changes) - self.ALLOWED_FIELDS
        if unknown:
            raise TaskValidationError(
                f"unsupported fields: {', '.join(sorted(unknown))}"
            )
        current = self.get(task_id)
        values = {
            "title": current.title,
            "description": current.description,
            "status": current.status,
        }
        values.update(changes)
        # Reuse create validation rules without persisting an extra record.
        if not isinstance(values["title"], str) or not values["title"].strip():
            raise TaskValidationError("title must be a non-empty string")
        if not isinstance(values["description"], str):
            raise TaskValidationError("description must be a string")
        if values["status"] not in self.ALLOWED_STATUSES:
            raise TaskValidationError("status is not supported")

        updated = Task(
            task_id=task_id,
            title=values["title"].strip(),
            description=values["description"],
            status=values["status"],
        )
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(f"task {task_id} was not found")
            self._tasks[task_id] = updated
        return updated


def run_smoke_tests() -> None:
    service = TaskService()
    task = service.create({"title": "Prepare capstone"})
    assert task.task_id == 1
    assert service.get(task.task_id).title == "Prepare capstone"
    updated = service.update(task.task_id, {"status": "in_progress"})
    assert updated.status == "in_progress"
    for payload in ({}, {"title": " "}, {"title": "x", "is_admin": True}):
        try:
            service.create(payload)
        except TaskValidationError:
            pass
        else:
            raise AssertionError(f"invalid payload accepted: {payload!r}")
    try:
        service.get(999)
    except TaskNotFoundError:
        pass
    else:
        raise AssertionError("missing task should raise TaskNotFoundError")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 83 task service smoke tests passed.")
