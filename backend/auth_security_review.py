"""Day 82: Framework-independent authentication and API security review.

These helpers demonstrate defensive decisions for interview practice. They
are not a substitute for a maintained authentication library or deployment
security review.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    user_id: str
    roles: frozenset[str]


def require_authenticated(principal: Principal | None) -> Principal:
    """Reject missing identity; authorization is a separate decision."""
    if principal is None or not principal.user_id.strip():
        raise PermissionError("authentication required")
    return principal


def can_access_resource(
    principal: Principal | None,
    owner_id: str,
    *,
    allowed_roles: frozenset[str] = frozenset(),
) -> bool:
    """Apply resource ownership or an explicitly allowed role."""
    if principal is None or not principal.user_id.strip():
        return False
    if principal.user_id == owner_id:
        return True
    return bool(principal.roles.intersection(allowed_roles))


def validate_page_size(value: int, maximum: int = 100) -> int:
    if maximum < 1:
        raise ValueError("maximum must be positive")
    if value < 1 or value > maximum:
        raise ValueError(f"page size must be between 1 and {maximum}")
    return value


def run_smoke_tests() -> None:
    owner = Principal("user-1", frozenset({"user"}))
    admin = Principal("user-2", frozenset({"admin"}))
    assert require_authenticated(owner) == owner
    assert can_access_resource(owner, "user-1")
    assert not can_access_resource(owner, "user-3")
    assert can_access_resource(admin, "user-3", allowed_roles=frozenset({"admin"}))
    assert not can_access_resource(None, "user-1")
    assert validate_page_size(20) == 20
    for invalid in (0, 101):
        try:
            validate_page_size(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-range page size must fail")
    try:
        require_authenticated(None)
    except PermissionError:
        pass
    else:
        raise AssertionError("missing principal must fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 82 authentication/security review passed.")
