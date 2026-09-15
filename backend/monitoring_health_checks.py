"""Day 46 — Monitoring, health checks, readiness, and liveness."""

from __future__ import annotations

from flask import Blueprint, current_app


health_bp = Blueprint("health", __name__)


@health_bp.get("/health/live")
def liveness():
    """Show that the process is alive and able to serve requests."""
    return {"status": "ok", "check": "liveness"}, 200


@health_bp.get("/health/ready")
def readiness():
    """Report whether the service is ready to receive production traffic."""
    checks = {"application": "ok"}

    database_checker = current_app.config.get("DATABASE_HEALTH_CHECK")
    if database_checker is not None:
        try:
            database_checker()
            checks["database"] = "ok"
        except Exception:  # pragma: no cover - dependency failure is external.
            checks["database"] = "failed"

    ready = all(value == "ok" for value in checks.values())
    return {
        "status": "ok" if ready else "not_ready",
        "check": "readiness",
        "dependencies": checks,
    }, 200 if ready else 503
