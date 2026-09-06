"""
Day 37 — Logging for Distributed Applications

Demonstrates application-level logging practices for distributed systems:
- Consistent log fields
- Correlation/request IDs
- JSON log records
- Exception context
- Avoiding secrets and large payloads in logs

The example uses only the Python standard library so the logging pattern can
be applied before introducing a centralized logging platform.
"""

from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from uuid import uuid4


correlation_id: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)


class JsonFormatter(logging.Formatter):
    """Format log records as compact JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
        }

        for field in ("http_method", "http_path", "status_code"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload)


def configure_logging() -> None:
    """Configure one JSON stream handler for the application."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)


def set_correlation_id(value: str | None = None) -> str:
    """Set or generate the correlation ID for the current execution context."""
    request_id = value or str(uuid4())
    correlation_id.set(request_id)
    return request_id


def log_request(method: str, path: str, status_code: int) -> None:
    """Log an HTTP request without recording sensitive request data."""
    logging.getLogger(__name__).info(
        "request_completed",
        extra={
            "http_method": method,
            "http_path": path,
            "status_code": status_code,
        },
    )


def demonstrate_distributed_logging() -> None:
    """Show how a request can carry one correlation ID across log events."""
    logger = logging.getLogger(__name__)
    set_correlation_id("req-123")

    logger.info("request_started")
    try:
        raise TimeoutError("database operation timed out")
    except TimeoutError:
        logger.exception("request_failed")

    log_request("GET", "/expenses/42", 504)


if __name__ == "__main__":
    configure_logging()
    demonstrate_distributed_logging()
