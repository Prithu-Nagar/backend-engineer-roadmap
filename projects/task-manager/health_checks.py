"""Day 46 — Task Manager health checks."""

from __future__ import annotations

from typing import Callable


def liveness_check() -> tuple[dict[str, str], int]:
    """Return a lightweight process liveness response."""
    return {"status": "ok", "check": "liveness"}, 200


def readiness_check(
    database_check: Callable[[], None] | None = None,
    redis_check: Callable[[], None] | None = None,
) -> tuple[dict, int]:
    """Return readiness based on required dependency checks."""
    checks: dict[str, str] = {"application": "ok"}

    for name, check in (("database", database_check), ("redis", redis_check)):
        if check is None:
            continue
        try:
            check()
            checks[name] = "ok"
        except Exception:  # pragma: no cover - dependency failure is external.
            checks[name] = "failed"

    ready = all(value == "ok" for value in checks.values())
    return {
        "status": "ok" if ready else "not_ready",
        "check": "readiness",
        "dependencies": checks,
    }, 200 if ready else 503
