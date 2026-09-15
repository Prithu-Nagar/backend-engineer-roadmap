"""Day 46 — Structured Task Manager logging."""

from __future__ import annotations

import json
import logging
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format records as JSON for centralized log collection."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field_name in (
            "request_id",
            "http_method",
            "http_path",
            "status_code",
            "duration_ms",
        ):
            if hasattr(record, field_name):
                payload[field_name] = getattr(record, field_name)
        return json.dumps(payload)


def configure_structured_logging() -> logging.Logger:
    """Configure idempotent structured logging for the Task Manager."""
    logger = logging.getLogger("task_manager")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


logger = configure_structured_logging()
