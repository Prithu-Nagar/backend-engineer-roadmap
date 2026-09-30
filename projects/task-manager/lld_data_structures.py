"""
Day 61 — Task Manager LLD Data Structures Review

Small domain-focused structures for reviewing composition, interfaces, and
service boundaries before introducing framework-specific implementation detail.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, Optional, Protocol


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    task_id: int
    title: str
    status: TaskStatus = TaskStatus.TODO
    assignee_id: Optional[int] = None
    dependencies: set[int] = field(default_factory=set)

    def complete(self) -> None:
        if self.status == TaskStatus.DONE:
            return
        self.status = TaskStatus.DONE


class TaskStore(Protocol):
    def get(self, task_id: int) -> Task:
        ...

    def save(self, task: Task) -> None:
        ...

    def list_for_assignee(self, assignee_id: int) -> Iterable[Task]:
        ...


class InMemoryTaskStore:
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise ValueError(f"Task {task_id} was not found") from exc

    def save(self, task: Task) -> None:
        self._tasks[task.task_id] = task

    def list_for_assignee(self, assignee_id: int) -> Iterable[Task]:
        return [
            task for task in self._tasks.values()
            if task.assignee_id == assignee_id
        ]

class TaskService:
    def __init__(self, store: TaskStore) -> None:
        self._store = store

    def complete_task(self, task_id: int) -> Task:
        task = self._store.get(task_id)
        if task.dependencies:
            incomplete = [
                dependency_id
                for dependency_id in task.dependencies
                if self._store.get(dependency_id).status != TaskStatus.DONE
            ]
            if incomplete:
                raise ValueError(
                    f"Task has incomplete dependencies: {incomplete}"
                )

        task.complete()
        self._store.save(task)
        return task


def main() -> None:
    store = InMemoryTaskStore()
    store.save(Task(1, "Define API contract", TaskStatus.DONE, assignee_id=7))
    store.save(Task(2, "Review LLD", assignee_id=7, dependencies={1}))

    service = TaskService(store)
    completed = service.complete_task(2)
    print(completed)
    print([task.title for task in store.list_for_assignee(7)])


if __name__ == "__main__":
    main()
