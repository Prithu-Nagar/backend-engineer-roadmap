"""
Day 80 — Backend weak-area repair.

A minimal service-layer exercise for validation, predictable errors, and
regression checks. This is in-memory interview practice, not production storage.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: int
    title: str
    status: str = "pending"


@dataclass
class TaskService:
    tasks: dict[int, Task] = field(default_factory=dict)
    next_id: int = 1

    def create(self, title: str) -> Task:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        normalized = title.strip()
        if len(normalized) > 200:
            raise ValueError("title must be at most 200 characters")
        task = Task(self.next_id, normalized)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise LookupError(f"task {task_id} was not found") from exc

    def update_status(self, task_id: int, status: str) -> Task:
        if status not in {"pending", "in_progress", "completed"}:
            raise ValueError("unsupported status")
        task = self.get(task_id)
        task.status = status
        return task


def run_smoke_tests() -> None:
    service = TaskService()
    task = service.create("  Repair validation  ")
    assert task.task_id == 1
    assert task.title == "Repair validation"
    assert service.update_status(1, "completed").status == "completed"

    for operation in (
        lambda: service.create(" "),
        lambda: service.create("x" * 201),
        lambda: service.get(999),
        lambda: service.update_status(1, "unknown"),
    ):
        try:
            operation()
        except (ValueError, LookupError):
            pass
        else:
            raise AssertionError("invalid operation must fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 80 backend weak-area repair passed.")
