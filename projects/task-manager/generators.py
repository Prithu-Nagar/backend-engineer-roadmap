"""
Day 18 - Task Manager Generators

Demonstrates lazy task processing using generator pipelines.
"""


def task_generator(tasks):
    """Yield tasks lazily one at a time."""
    for task in tasks:
        yield task


def completed_tasks(tasks):
    """Yield only completed tasks."""
    for task in tasks:
        if task.get("completed") is True:
            yield task


def incomplete_tasks(tasks):
    """Yield only incomplete tasks."""
    for task in tasks:
        if task.get("completed") is False:
            yield task


def tasks_by_priority(tasks, minimum_priority):
    """Yield tasks meeting the minimum priority."""
    for task in tasks:
        if task.get("priority", 0) >= minimum_priority:
            yield task


def task_pipeline(tasks, minimum_priority=None, completed=None):
    """
    Build a lazy task-processing pipeline.

    The input is never converted into a complete intermediate list.
    """
    result = task_generator(tasks)

    if completed is True:
        result = completed_tasks(result)
    elif completed is False:
        result = incomplete_tasks(result)

    if minimum_priority is not None:
        result = tasks_by_priority(
            result,
            minimum_priority,
        )

    yield from result