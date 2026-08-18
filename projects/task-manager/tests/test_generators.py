"""Day 18 tests for generator-based task processing."""

from pathlib import Path
import importlib.util


TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]
GENERATORS_PATH = TASK_MANAGER_DIR / "generators.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_generators",
    GENERATORS_PATH,
)

assert spec is not None
assert spec.loader is not None

generators = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generators)


TASKS = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False,
        "priority": 3,
    },
    {
        "id": 2,
        "title": "Write tests",
        "completed": True,
        "priority": 5,
    },
    {
        "id": 3,
        "title": "Study SQL",
        "completed": False,
        "priority": 4,
    },
]


def test_task_generator_is_lazy():
    result = generators.task_generator(TASKS)

    assert hasattr(result, "__next__")
    assert next(result) == TASKS[0]


def test_completed_tasks():
    result = list(generators.completed_tasks(TASKS))

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_incomplete_tasks():
    result = list(generators.incomplete_tasks(TASKS))

    assert [task["id"] for task in result] == [1, 3]


def test_priority_pipeline():
    result = list(
        generators.task_pipeline(
            TASKS,
            minimum_priority=4,
        )
    )

    assert [task["id"] for task in result] == [2, 3]


def test_combined_generator_pipeline():
    result = list(
        generators.task_pipeline(
            TASKS,
            minimum_priority=4,
            completed=False,
        )
    )

    assert [task["id"] for task in result] == [3]