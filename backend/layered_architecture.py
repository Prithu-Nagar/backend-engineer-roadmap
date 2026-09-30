"""
Day 61 — Layered Backend Architecture

A framework-neutral example of presentation, application, domain, and
infrastructure boundaries. Dependencies point inward through small interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str


class TaskRepository(Protocol):
    def get(self, task_id: int) -> Task:
        ...


class InMemoryTaskRepository:
    def __init__(self, tasks: dict[int, Task]) -> None:
        self._tasks = tasks

    def get(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise ValueError("task not found")
        return self._tasks[task_id]


class TaskService:
    """Application layer: coordinates a use case using domain-facing contracts."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def get_task(self, task_id: int) -> dict[str, object]:
        task = self._repository.get(task_id)
        return {"id": task.task_id, "title": task.title}


class TaskController:
    """Presentation layer: converts a request-shaped input into a service call."""

    def __init__(self, service: TaskService) -> None:
        self._service = service

    def get(self, task_id: int) -> dict[str, object]:
        return self._service.get_task(task_id)


def build_application() -> TaskController:
    repository = InMemoryTaskRepository({1: Task(1, "Review layered architecture")})
    service = TaskService(repository)
    return TaskController(service)


if __name__ == "__main__":
    print(build_application().get(1))
