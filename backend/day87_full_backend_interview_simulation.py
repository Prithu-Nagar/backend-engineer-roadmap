"""Day 87 — Full backend interview simulation helpers.

Use these functions as a short coding prompt. In an interview, explain the
contract, failure modes, complexity, and production trade-offs before coding.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiError:
    code: str
    message: str
    request_id: str
    status_code: int


def validate_pagination(page: int, page_size: int, max_page_size: int = 100) -> tuple[int, int]:
    """Validate one-based pagination and cap page size."""
    if page < 1:
        raise ValueError("page must be at least 1")
    if page_size < 1:
        raise ValueError("page_size must be at least 1")
    if max_page_size < 1:
        raise ValueError("max_page_size must be at least 1")
    return page, min(page_size, max_page_size)


def make_error(code: str, message: str, request_id: str, status_code: int) -> ApiError:
    """Build a stable client-safe error object."""
    if not code or not request_id:
        raise ValueError("code and request_id are required")
    if status_code < 400 or status_code > 599:
        raise ValueError("status_code must be an error status")
    return ApiError(code, message, request_id, status_code)


def owns_resource(authenticated_user_id: str, owner_id: str) -> bool:
    """Return whether a non-empty authenticated identity owns the resource."""
    return bool(authenticated_user_id) and authenticated_user_id == owner_id


def run_smoke_tests() -> None:
    assert validate_pagination(1, 500) == (1, 100)
    try:
        validate_pagination(0, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("page zero must be rejected")
    error = make_error("NOT_FOUND", "Resource not found.", "req-1", 404)
    assert error.status_code == 404
    assert owns_resource("user-1", "user-1")
    assert not owns_resource("user-1", "user-2")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 87 backend interview simulation checks passed.")
