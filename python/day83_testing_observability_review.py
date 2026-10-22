"""Day 83 — Python testing and observability review."""

from __future__ import annotations

import logging
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServiceMetrics:
    """Small in-process metrics collector for a service demonstration."""

    requests_total: int = 0
    errors_total: int = 0
    duration_total_ms: float = 0.0
    status_counts: Counter[int] = field(default_factory=Counter)

    def observe(self, status_code: int, duration_ms: float) -> None:
        if status_code < 100 or status_code > 599:
            raise ValueError("status_code must be a valid HTTP status")
        if duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")
        self.requests_total += 1
        self.errors_total += int(status_code >= 500)
        self.duration_total_ms += duration_ms
        self.status_counts[status_code] += 1

    def snapshot(self) -> dict[str, Any]:
        average = (
            self.duration_total_ms / self.requests_total
            if self.requests_total
            else 0.0
        )
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "average_duration_ms": round(average, 2),
            "status_counts": dict(self.status_counts),
        }


def run_observed_operation(
    operation_name: str,
    operation,
    logger: logging.Logger,
    metrics: ServiceMetrics,
) -> Any:
    """Execute an operation, log its outcome, and record its duration."""
    started = time.perf_counter()
    status_code = 200
    try:
        result = operation()
        return result
    except Exception:
        status_code = 500
        logger.exception("operation_failed", extra={"operation": operation_name})
        raise
    finally:
        duration_ms = (time.perf_counter() - started) * 1000
        metrics.observe(status_code, duration_ms)
        logger.info(
            "operation_completed",
            extra={
                "operation": operation_name,
                "status_code": status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )


def run_smoke_tests() -> None:
    logger = logging.getLogger("day83.review")
    metrics = ServiceMetrics()
    assert run_observed_operation("sum", lambda: 2 + 3, logger, metrics) == 5
    assert metrics.requests_total == 1
    assert metrics.errors_total == 0
    try:
        run_observed_operation(
            "failure", lambda: (_ for _ in ()).throw(RuntimeError("expected")),
            logger, metrics,
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError("the operation exception should propagate")
    snapshot = metrics.snapshot()
    assert snapshot["requests_total"] == 2
    assert snapshot["errors_total"] == 1
    assert snapshot["status_counts"] == {200: 1, 500: 1}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_smoke_tests()
    print("Day 83 testing/observability review passed.")
