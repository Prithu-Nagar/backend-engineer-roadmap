"""Day 86 — Backend security hardening review helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityConfig:
    environment: str
    debug: bool
    allowed_origins: tuple[str, ...]
    trusted_hosts: tuple[str, ...]


def validate_security_config(config: SecurityConfig) -> list[str]:
    """Return actionable configuration issues without exposing secret values."""
    issues: list[str] = []
    production = config.environment.strip().lower() == "production"
    if production and config.debug:
        issues.append("debug mode must be disabled in production")
    if production and not config.allowed_origins:
        issues.append("production CORS origins must be explicitly configured")
    if production and not config.trusted_hosts:
        issues.append("production trusted hosts must be explicitly configured")
    if "*" in config.allowed_origins:
        issues.append("wildcard CORS origin is not allowed by this policy")
    return issues


def owns_resource(authenticated_user_id: str, resource_owner_id: str) -> bool:
    """Check ownership after authentication; real queries should enforce it atomically."""
    return bool(authenticated_user_id) and authenticated_user_id == resource_owner_id


def safe_error_payload(code: str, message: str, request_id: str) -> dict[str, object]:
    """Return a client-safe error shape; never include stack traces or secret values."""
    return {
        "error": {"code": code, "message": message, "request_id": request_id}
    }


def run_smoke_tests() -> None:
    production = SecurityConfig("production", True, ("*",), ())
    issues = validate_security_config(production)
    assert len(issues) == 3
    assert not validate_security_config(
        SecurityConfig("production", False, ("https://app.example",), ("api.example",))
    )
    assert owns_resource("user-1", "user-1")
    assert not owns_resource("user-1", "user-2")
    payload = safe_error_payload("NOT_FOUND", "Resource not found.", "req-123")
    assert "traceback" not in str(payload).lower()
    assert payload["error"]["request_id"] == "req-123"


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 86 backend security review checks passed.")
