"""
Day 65 — API Versioning

A framework-neutral versioning example for a backend API. It demonstrates
explicit request routing, version-specific serializers, and a compatibility
boundary so clients can migrate without silently changing response contracts.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    completed: bool


class TaskApiV1:
    """Legacy response contract kept stable for existing clients."""

    @staticmethod
    def serialize(task: Task) -> dict[str, object]:
        return {
            "id": task.task_id,
            "title": task.title,
            "completed": task.completed,
        }


class TaskApiV2:
    """New response contract with a nested status representation."""

    @staticmethod
    def serialize(task: Task) -> dict[str, object]:
        return {
            "id": task.task_id,
            "title": task.title,
            "status": "completed" if task.completed else "pending",
        }


class UnsupportedApiVersion(ValueError):
    """Raised when a client requests a version the service does not support."""


class TaskApiRouter:
    """Selects an explicit version without duplicating domain logic."""

    SUPPORTED_VERSIONS = frozenset({"v1", "v2"})

    def serialize(self, version: str, task: Task) -> dict[str, object]:
        normalized = version.lower().strip()
        if normalized not in self.SUPPORTED_VERSIONS:
            raise UnsupportedApiVersion(f"unsupported API version: {version}")

        if normalized == "v1":
            return TaskApiV1.serialize(task)
        return TaskApiV2.serialize(task)


def main() -> None:
    task = Task(42, "Design URL Shortener", False)
    router = TaskApiRouter()

    print("v1:", router.serialize("v1", task))
    print("v2:", router.serialize("v2", task))


if __name__ == "__main__":
    main()
