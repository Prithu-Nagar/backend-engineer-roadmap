"""
Day 61 — SOLID Principles in Python

A small backend-oriented example showing single responsibility, open/closed
design, substitutability, interface segregation, dependency inversion, and
composition without coupling the application service to concrete adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Task:  # Single Responsibility: task data only.
    task_id: int
    title: str
    completed: bool = False


class TaskRepository(Protocol):  # Interface used by the application layer.
    def get(self, task_id: int) -> Task:
        ...


class InMemoryTaskRepository:
    def __init__(self, tasks: dict[int, Task]) -> None:
        self._tasks = tasks

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise ValueError(f"Task {task_id} was not found") from exc


class TaskNotifier(ABC):
    """Small abstraction so notification implementations remain substitutable."""

    @abstractmethod
    def send(self, task: Task) -> str:
        raise NotImplementedError


class ConsoleNotifier(TaskNotifier):
    def send(self, task: Task) -> str:
        return f"notified: {task.task_id} — {task.title}"


class TaskService:
    """Application policy composed from abstractions rather than concrete adapters."""

    def __init__(self, repository: TaskRepository, notifier: TaskNotifier) -> None:
        self._repository = repository
        self._notifier = notifier

    def complete_task(self, task_id: int) -> str:
        task = self._repository.get(task_id)
        completed = Task(task.task_id, task.title, completed=True)
        return self._notifier.send(completed)


def main() -> None:
    repository = InMemoryTaskRepository({1: Task(1, "Review LLD boundaries")})
    service = TaskService(repository, ConsoleNotifier())
    print(service.complete_task(1))


if __name__ == "__main__":
    main()
