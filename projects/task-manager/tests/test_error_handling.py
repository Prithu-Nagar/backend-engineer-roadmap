"""Day 18 tests for standardized Task Manager errors."""

from pathlib import Path
import importlib.util


TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]
ERROR_HANDLING_PATH = TASK_MANAGER_DIR / "error_handling.py"

spec = importlib.util.spec_from_file_location(
    "task_manager_error_handling",
    ERROR_HANDLING_PATH,
)

assert spec is not None
assert spec.loader is not None

error_handling = importlib.util.module_from_spec(spec)
spec.loader.exec_module(error_handling)


def test_task_not_found_error():
    response, status_code = error_handling.TASK_NOT_FOUND.to_response()

    assert status_code == 404
    assert response["error"]["code"] == "TASK_NOT_FOUND"
    assert response["error"]["message"] == (
        "The requested task was not found."
    )


def test_forbidden_error():
    response, status_code = error_handling.FORBIDDEN.to_response()

    assert status_code == 403
    assert response["error"]["code"] == "FORBIDDEN"


def test_bad_request_error():
    response, status_code = error_handling.BAD_REQUEST.to_response()

    assert status_code == 400
    assert response["error"]["code"] == "BAD_REQUEST"