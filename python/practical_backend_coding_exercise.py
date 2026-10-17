"""
Day 78 — Practical Backend Coding Exercise

A small, framework-independent task service for timed backend interview practice.
Run this file directly to execute the built-in smoke checks.

Exercise goals:
- Validate input at the service boundary.
- Keep persistence behind a repository abstraction.
- Implement create, retrieve, update-status, and bounded pagination.
- Use deterministic behavior and explicit errors.
"""

from dataclasses import dataclass
from typing import ClassVar, Protocol


class TaskNotFoundError(LookupError):
    """Raised when a requested task does not exist."""


class TaskValidationError(ValueError):
    """Raised when task input is invalid."""


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    status: str = "pending"


class TaskRepository(Protocol):
    def add(self, title: str) -> Task: ...
    def get(self, task_id: int) -> Task: ...
    def list_page(self, offset: int, limit: int) -> list[Task]: ...
    def update_status(self, task_id: int, status: str) -> Task: ...


class InMemoryTaskRepository:
    """Deterministic repository for an exercise; not durable storage."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str) -> Task:
        task = Task(task_id=self._next_id, title=title)
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise TaskNotFoundError(f"Task {task_id} was not found") from exc

    def list_page(self, offset: int, limit: int) -> list[Task]:
        ordered = sorted(self._tasks.values(), key=lambda task: task.task_id)
        return ordered[offset : offset + limit]

    def update_status(self, task_id: int, status: str) -> Task:
        current = self.get(task_id)
        updated = Task(current.task_id, current.title, status)
        self._tasks[task_id] = updated
        return updated


class TaskService:
    """Apply input validation and business rules before repository calls."""

    ALLOWED_STATUSES: ClassVar[set[str]] = {"pending", "in_progress", "completed"}

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create_task(self, title: str) -> Task:
        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError("title must be a non-empty string")
        if len(title.strip()) > 200:
            raise TaskValidationError("title must contain at most 200 characters")
        return self._repository.add(title.strip())

    def get_task(self, task_id: int) -> Task:
        if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id < 1:
            raise TaskValidationError("task_id must be a positive integer")
        return self._repository.get(task_id)

    def list_tasks(self, offset: int = 0, limit: int = 20) -> list[Task]:
        if not isinstance(offset, int) or offset < 0:
            raise TaskValidationError("offset must be a non-negative integer")
        if not isinstance(limit, int) or not 1 <= limit <= 100:
            raise TaskValidationError("limit must be between 1 and 100")
        return self._repository.list_page(offset, limit)

    def change_status(self, task_id: int, status: str) -> Task:
        self.get_task(task_id)
        if status not in self.ALLOWED_STATUSES:
            raise TaskValidationError(
                f"status must be one of: {', '.join(sorted(self.ALLOWED_STATUSES))}"
            )
        return self._repository.update_status(task_id, status)


def _smoke_check() -> None:
    service = TaskService(InMemoryTaskRepository())
    first = service.create_task(" Prepare interview ")
    assert first.task_id == 1
    assert first.title == "Prepare interview"
    assert service.get_task(1).status == "pending"
    assert service.change_status(1, "completed").status == "completed"
    assert len(service.list_tasks(offset=0, limit=10)) == 1

    try:
        service.create_task("   ")
    except TaskValidationError:
        pass
    else:
        raise AssertionError("Blank titles must be rejected")

    try:
        service.get_task(99)
    except TaskNotFoundError:
        pass
    else:
        raise AssertionError("Missing tasks must raise TaskNotFoundError")


if __name__ == "__main__":
    _smoke_check()
    print("TaskService smoke checks passed.")
