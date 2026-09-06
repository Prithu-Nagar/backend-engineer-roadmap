"""
Day 37 — Structured Logging & Correlation IDs

A small Flask-oriented logging helper that attaches a correlation ID to each
request and emits structured JSON logs. The correlation ID is the bridge
between application logs, database logs, and distributed traces.
"""

from __future__ import annotations

import json
import logging
from uuid import uuid4

from flask import Flask, g, request


class JsonFormatter(logging.Formatter):
    """Format application log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", None),
        }

        for field in ("http_method", "http_path", "status_code"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)

        return json.dumps(payload)


def configure_structured_logging() -> None:
    """Install a JSON formatter on the application logger."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False


def create_app() -> Flask:
    """Create a small Flask app demonstrating correlation-ID logging."""
    app = Flask(__name__)
    configure_structured_logging()

    logger = logging.getLogger("expense_tracker")

    @app.before_request
    def attach_correlation_id() -> None:
        incoming = request.headers.get("X-Correlation-ID")
        g.correlation_id = incoming or str(uuid4())

    @app.after_request
    def add_correlation_header(response):
        response.headers["X-Correlation-ID"] = g.correlation_id
        logger.info(
            "request_completed",
            extra={"correlation_id": g.correlation_id},
        )
        return response

    @app.get("/health")
    def health():
        logger.info(
            "health_check",
            extra={"correlation_id": g.correlation_id},
        )
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
