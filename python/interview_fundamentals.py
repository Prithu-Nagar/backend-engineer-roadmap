"""Small, runnable examples for common Python interview fundamentals."""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


def normalize_names(names: list[str] | None = None) -> list[str]:
    """Avoid mutable default arguments by creating a fresh list per call."""
    if names is None:
        names = []
    return [name.strip().title() for name in names]


def first_seen_counts(values: list[T]) -> dict[T, int]:
    """Count hashable values while preserving first-insertion order."""
    counts: dict[T, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def positive_numbers(values: list[int]) -> Iterator[int]:
    """Yield positive values lazily instead of building an intermediate list."""
    for value in values:
        if value > 0:
            yield value


@dataclass(frozen=True)
class TaskSummary:
    task_id: int
    title: str
    completed: bool = False


def summarize_task(task: TaskSummary) -> str:
    """Return a compact summary; frozen dataclasses prevent field reassignment."""
    status = "completed" if task.completed else "open"
    return f"#{task.task_id}: {task.title} ({status})"


def safe_divide(numerator: float, denominator: float) -> float:
    """Raise a clear error for invalid input instead of hiding the failure."""
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


if __name__ == "__main__":
    assert normalize_names(["  ada lovelace "]) == ["Ada Lovelace"]
    assert normalize_names() == []
    assert first_seen_counts(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert list(positive_numbers([-1, 0, 2, 3])) == [2, 3]
    assert summarize_task(TaskSummary(7, "Prepare interview")) == (
        "#7: Prepare interview (open)"
    )
    assert safe_divide(6, 2) == 3
    print("Python interview fundamentals examples passed.")
