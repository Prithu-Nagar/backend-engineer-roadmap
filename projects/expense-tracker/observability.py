"""
Day 37 — Expense Tracker Observability

Adds a lightweight observability layer for the Expense Tracker:
- Correlation IDs
- Structured request logging
- Timing information
- Safe, bounded event fields

The module is framework-agnostic so it can be connected to Flask middleware,
a tracing library, or a centralized logging platform later.
"""

from __future__ import annotations

import json
import logging
import time
from contextvars import ContextVar
from uuid import uuid4


correlation_id: ContextVar[str] = ContextVar(
    "expense_tracker_correlation_id",
    default="-",
)


class JsonFormatter(logging.Formatter):
    """Serialize Expense Tracker log events as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
        }

        for field in ("http_method", "http_path", "status_code", "duration_ms"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)

        return json.dumps(payload)


def configure_logging() -> None:
    """Configure structured logs for the Expense Tracker."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False


def start_request(request_id: str | None = None) -> str:
    """Create the correlation context for one request."""
    value = request_id or str(uuid4())
    correlation_id.set(value)
    return value


def record_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
) -> None:
    """Emit one bounded structured request event."""
    logging.getLogger("expense_tracker").info(
        "request_completed",
        extra={
            "http_method": method,
            "http_path": path,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )


def timed_request(method: str, path: str, status_code: int = 200) -> None:
    """Demonstrate request timing and structured event emission."""
    start = time.perf_counter()
    time.sleep(0.001)
    duration_ms = (time.perf_counter() - start) * 1000

    record_request(
        method,
        path,
        status_code,
        duration_ms,
    )


if __name__ == "__main__":
    configure_logging()
    start_request("expense-req-001")
    timed_request("GET", "/expenses")
