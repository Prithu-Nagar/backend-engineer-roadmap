"""
Logging Fundamentals

Topics:
- Log levels
- Logger
- Handler
- Formatter
- Exception logging
- Structured logging concepts
"""

import json
import logging


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure basic application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def log_levels() -> None:
    """Demonstrate the standard Python logging levels."""
    logger.debug("Debug message")
    logger.info("Application started")
    logger.warning("Configuration value is missing; using default")
    logger.error("An error occurred while processing the request")
    logger.critical("Critical application failure")


def demonstrate_exception_logging() -> None:
    """Demonstrate logging an exception with traceback information."""
    try:
        result = 10 / 0
        logger.info("Result: %s", result)
    except ZeroDivisionError:
        logger.exception("Failed to perform division")


def structured_log(event: str, **fields) -> None:
    """Write a structured log record as JSON."""
    record = {
        "event": event,
        **fields,
    }

    logger.info(json.dumps(record))


if __name__ == "__main__":
    configure_logging()

    log_levels()
    demonstrate_exception_logging()

    structured_log(
        "task_created",
        user_id=101,
        task_id=5001,
        status="success",
    )