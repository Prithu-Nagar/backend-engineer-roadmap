"""Day 46 — Production Logging and Metrics.

Demonstrates structured logging plus lightweight in-process metrics that can
be exported to a real monitoring system later.
"""

from __future__ import annotations

import json
import logging
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


class JsonFormatter(logging.Formatter):
    """Render log records as JSON for centralized log ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field_name in ("request_id", "method", "path", "status_code", "duration_ms"):
            if hasattr(record, field_name):
                payload[field_name] = getattr(record, field_name)
        return json.dumps(payload)


def configure_logging(logger_name: str = "production_app") -> logging.Logger:
    """Create an idempotent JSON logger suitable for container stdout."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


@dataclass
class RequestMetrics:
    """Small in-process metric collector for request-level examples."""

    requests_total: int = 0
    errors_total: int = 0
    total_duration_ms: float = 0.0
    status_counts: Counter[int] = field(default_factory=Counter)

    def observe(self, status_code: int, duration_ms: float) -> None:
        self.requests_total += 1
        self.total_duration_ms += duration_ms
        self.status_counts[status_code] += 1
        if status_code >= 500:
            self.errors_total += 1

    def snapshot(self) -> dict[str, Any]:
        """Return serializable metrics for inspection or export."""
        average = (
            self.total_duration_ms / self.requests_total
            if self.requests_total
            else 0.0
        )
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "average_duration_ms": round(average, 2),
            "status_counts": dict(self.status_counts),
        }


def record_request(
    logger: logging.Logger,
    metrics: RequestMetrics,
    method: str,
    path: str,
    status_code: int,
    started_at: float,
    request_id: str,
) -> None:
    """Record request metrics and emit one structured completion event."""
    duration_ms = (time.perf_counter() - started_at) * 1000
    metrics.observe(status_code, duration_ms)
    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )


if __name__ == "__main__":
    logger = configure_logging()
    metrics = RequestMetrics()
    started = time.perf_counter()
    time.sleep(0.01)
    record_request(logger, metrics, "GET", "/health/live", 200, started, "req-46")
    logger.info("metrics_snapshot: %s", metrics.snapshot())
