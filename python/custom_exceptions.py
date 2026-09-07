"""
Day 38 — Error Taxonomy and Custom Exceptions

Demonstrates a small exception hierarchy for backend services. The hierarchy
separates client/domain failures from transient dependency failures so callers
can decide which errors are safe to retry.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ServiceError(Exception):
    """Base application error that can be translated at a service boundary."""

    code: str
    message: str
    status_code: int = 500
    retryable: bool = False

    def __post_init__(self) -> None:
        super().__init__(self.message)


class ValidationError(ServiceError):
    """The caller supplied invalid input."""

    def __init__(self, message: str = "The request is invalid.") -> None:
        super().__init__("VALIDATION_ERROR", message, 400, False)


class NotFoundError(ServiceError):
    """The requested domain resource does not exist."""

    def __init__(self, resource: str = "resource") -> None:
        super().__init__("NOT_FOUND", f"The requested {resource} was not found.", 404, False)


class ConflictError(ServiceError):
    """The operation conflicts with current resource state."""

    def __init__(self, message: str = "The request conflicts with the current state.") -> None:
        super().__init__("CONFLICT", message, 409, False)


class DependencyUnavailableError(ServiceError):
    """A downstream dependency failed in a potentially transient way."""

    def __init__(self, dependency: str) -> None:
        super().__init__(
            "DEPENDENCY_UNAVAILABLE",
            f"The {dependency} dependency is temporarily unavailable.",
            503,
            True,
        )


def error_payload(error: ServiceError) -> dict[str, object]:
    """Create a safe response payload without exposing internal details."""
    return {
        "error": {
            "code": error.code,
            "message": error.message,
            "retryable": error.retryable,
        }
    }


def load_expense(expense_id: int) -> dict[str, object]:
    """Example service operation with explicit domain error handling."""
    if expense_id <= 0:
        raise ValidationError("expense_id must be positive")

    if expense_id != 1:
        raise NotFoundError("expense")

    return {"id": 1, "category": "travel", "amount": 2500.0}


if __name__ == "__main__":
    try:
        load_expense(2)
    except ServiceError as error:
        print(error_payload(error))
