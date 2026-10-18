"""
Day 79 — Backend debugging exercise.

A deliberately faulty in-memory service is provided for interview practice.
Identify the defects before consulting the corrected implementation below.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: int
    title: str
    status: str = "pending"


@dataclass
class TaskStore:
    tasks: dict[int, Task] = field(default_factory=dict)
    next_id: int = 1

    def create(self, title: str) -> Task:
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("title must not be empty")

        task = Task(task_id=self.next_id, title=normalized_title)
        self.tasks[task.task_id] = task
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
    store = TaskStore()
    first = store.create("  Fix API timeout  ")
    second = store.create("Add regression test")

    assert first.task_id == 1
    assert first.title == "Fix API timeout"
    assert second.task_id == 2
    assert store.update_status(1, "completed").status == "completed"

    for operation in (
        lambda: store.create("   "),
        lambda: store.get(999),
        lambda: store.update_status(1, "unknown"),
    ):
        try:
            operation()
        except (ValueError, LookupError):
            pass
        else:
            raise AssertionError("invalid operation should raise an exception")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 79 backend debugging exercise passed.")
