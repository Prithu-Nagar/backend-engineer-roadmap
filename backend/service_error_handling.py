"""
Day 38 — Robust Error Handling Across Services

Shows how a backend can normalize domain and dependency failures at a service
boundary without exposing internal exception details to API clients.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Callable, TypeVar

from flask import Flask, jsonify


logger = logging.getLogger(__name__)
app = Flask(__name__)

T = TypeVar("T")


@dataclass
class ServiceFailure(Exception):
    """Safe, transport-independent error raised by service code."""

    code: str
    message: str
    status_code: int
    retryable: bool = False

    def __post_init__(self) -> None:
        super().__init__(self.message)


class DependencyFailure(ServiceFailure):
    def __init__(self, dependency: str) -> None:
        super().__init__(
            "DEPENDENCY_UNAVAILABLE",
            f"The {dependency} dependency is temporarily unavailable.",
            503,
            True,
        )


def call_dependency(operation: Callable[[], T]) -> T:
    """Translate low-level dependency failures into a stable service error."""
    try:
        return operation()
    except TimeoutError as error:
        raise DependencyFailure("database") from error
    except ConnectionError as error:
        raise DependencyFailure("database") from error


def error_response(error: ServiceFailure):
    return jsonify(
        {
            "error": {
                "code": error.code,
                "message": error.message,
                "retryable": error.retryable,
            }
        }
    ), error.status_code


@app.errorhandler(ServiceFailure)
def handle_service_failure(error: ServiceFailure):
    logger.warning(
        "service_failure code=%s retryable=%s",
        error.code,
        error.retryable,
    )
    return error_response(error)


@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    # Log the internal exception for operators, but return a generic response.
    logger.exception("unexpected_service_error")
    return error_response(
        ServiceFailure(
            "INTERNAL_SERVER_ERROR",
            "An unexpected error occurred.",
            500,
            False,
        )
    )


@app.get("/expense/<int:expense_id>")
def get_expense(expense_id: int):
    if expense_id <= 0:
        raise ServiceFailure("VALIDATION_ERROR", "expense_id must be positive", 400)

    return jsonify({"id": expense_id, "status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
