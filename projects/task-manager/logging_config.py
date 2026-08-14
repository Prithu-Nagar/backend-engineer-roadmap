"""Logging configuration for the Task Manager project."""

import logging


def configure_logging() -> logging.Logger:
    """Set up a basic logger for the Task Manager API."""
    logger = logging.getLogger("task_manager")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = configure_logging()


if __name__ == "__main__":
    logger.info("Task Manager logging initialized")
