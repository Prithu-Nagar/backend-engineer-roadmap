"""Day 81 — API architecture review: stable contracts and consistent errors."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    method: str
    path: str
    version: str
    auth_required: bool

    def validate(self) -> None:
        if self.method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            raise ValueError("unsupported HTTP method")
        if not self.path.startswith("/") or " " in self.path:
            raise ValueError("path must be an absolute URL path without spaces")
        if self.version not in {"v1", "v2"}:
            raise ValueError("unsupported API version")


def success_response(data: object, *, request_id: str) -> dict[str, object]:
    """Create a predictable success envelope; transport code sets HTTP status."""
    if not request_id.strip():
        raise ValueError("request_id must not be empty")
    return {"data": data, "error": None, "meta": {"request_id": request_id}}


def error_response(code: str, message: str, *, request_id: str) -> dict[str, object]:
    """Return a stable client-facing error shape without internal exception details."""
    if not code.strip() or not message.strip() or not request_id.strip():
        raise ValueError("code, message, and request_id are required")
    return {
        "data": None,
        "error": {"code": code, "message": message},
        "meta": {"request_id": request_id},
    }


def run_smoke_tests() -> None:
    Endpoint("GET", "/api/v1/tasks", "v1", True).validate()
    assert success_response({"id": 1}, request_id="req-123")["error"] is None
    assert error_response("NOT_FOUND", "Task not found", request_id="req-123")["data"] is None
    for endpoint in (
        Endpoint("TRACE", "/tasks", "v1", False),
        Endpoint("GET", "tasks", "v1", False),
        Endpoint("GET", "/tasks", "v3", False),
    ):
        try:
            endpoint.validate()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid endpoint must fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 81 API architecture review passed.")
