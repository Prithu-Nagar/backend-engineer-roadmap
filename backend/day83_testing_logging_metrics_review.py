"""Day 83 — Backend testing, logging, and metrics review.

This module is framework-independent so it can be reused by Flask, Django,
or FastAPI services.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass
class RequestMetrics:
    """Process-local request counters for examples and tests."""

    requests_total: int = 0
    errors_total: int = 0
    duration_total_ms: float = 0.0
    status_counts: dict[int, int] = field(default_factory=dict)

    def record(self, status_code: int, duration_ms: float) -> None:
        if not 100 <= status_code <= 599:
            raise ValueError("status_code must be between 100 and 599")
        if duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")
        self.requests_total += 1
        self.errors_total += int(status_code >= 500)
        self.duration_total_ms += duration_ms
        self.status_counts[status_code] = self.status_counts.get(status_code, 0) + 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "average_duration_ms": round(
                self.duration_total_ms / self.requests_total, 2
            ) if self.requests_total else 0.0,
            "status_counts": dict(self.status_counts),
        }


def observe_call(
    name: str,
    operation: Callable[[], T],
    logger: logging.Logger,
    metrics: RequestMetrics,
) -> T:
    """Log operation outcome and latency while preserving return/errors."""
    started = time.perf_counter()
    status = 200
    try:
        result = operation()
        return result
    except Exception:
        status = 500
        logger.exception("backend_operation_failed", extra={"operation": name})
        raise
    finally:
        elapsed_ms = (time.perf_counter() - started) * 1000
        metrics.record(status, elapsed_ms)
        logger.info(
            "backend_operation_completed",
            extra={
                "operation": name,
                "status_code": status,
                "duration_ms": round(elapsed_ms, 2),
            },
        )


def run_smoke_tests() -> None:
    logger = logging.getLogger("backend.day83")
    metrics = RequestMetrics()
    assert observe_call("health", lambda: {"status": "ok"}, logger, metrics) == {
        "status": "ok"
    }
    assert metrics.snapshot()["requests_total"] == 1
    assert metrics.snapshot()["errors_total"] == 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_smoke_tests()
    print("Day 83 backend review passed.")
