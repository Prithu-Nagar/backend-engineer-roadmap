"""Day 88 — Backend weak-area repair.

Framework-independent checks for API contracts, ownership, and safe error
responses. Adapt these helpers to the capstone's actual service layer.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiError:
    code: str
    message: str
    request_id: str
    status_code: int


def validate_pagination(page: int, page_size: int, maximum: int = 100) -> tuple[int, int]:
    if page < 1 or page_size < 1 or maximum < 1:
        raise ValueError("pagination values must be positive")
    return page, min(page_size, maximum)


def make_error(code: str, message: str, request_id: str, status_code: int) -> ApiError:
    """Create a stable client-safe error contract."""
    if not code.strip() or not request_id.strip():
        raise ValueError("code and request_id are required")
    if not 400 <= status_code <= 599:
        raise ValueError("status_code must be an error status")
    return ApiError(code, message, request_id, status_code)


def owns_resource(authenticated_user_id: str | None, owner_id: str) -> bool:
    """Deny access when identity is absent; compare resource ownership."""
    return bool(authenticated_user_id) and authenticated_user_id == owner_id


def run_smoke_tests() -> None:
    assert validate_pagination(1, 500) == (1, 100)
    error = make_error("NOT_FOUND", "Resource not found.", "req-123", 404)
    assert error.status_code == 404
    assert owns_resource("user-1", "user-1")
    assert not owns_resource(None, "user-1")
    assert not owns_resource("user-1", "user-2")
    try:
        make_error("BAD_REQUEST", "Invalid input.", "req-1", 200)
    except ValueError:
        pass
    else:
        raise AssertionError("success status must not be an API error")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 88 backend repair smoke tests passed.")
