"""
Day 38 — Expense Tracker Reliability

Adds a small reliability boundary for transient dependency failures. The
implementation uses bounded retries with exponential backoff and jitter and
requires the caller to decide whether the operation is safe to repeat.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


class TransientDependencyError(Exception):
    """A dependency failure that may succeed on a later attempt."""


def with_retry(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    base_delay: float = 0.05,
    max_delay: float = 1.0,
    sleeper: Callable[[float], None] = time.sleep,
    random_value: Callable[[], float] = random.random,
) -> T:
    """Retry a known-transient operation with exponential backoff and jitter."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    if base_delay < 0 or max_delay < 0:
        raise ValueError("delays must not be negative")

    for attempt in range(attempts):
        try:
            return operation()
        except TransientDependencyError:
            if attempt == attempts - 1:
                raise

            backoff = min(max_delay, base_delay * (2**attempt))
            jittered_delay = random_value() * backoff
            sleeper(jittered_delay)

    raise RuntimeError("unreachable")


def fetch_expense_from_dependency() -> dict[str, object]:
    """Example dependency call that succeeds without requiring Redis/HTTP."""
    return {"id": 1, "category": "travel", "amount": 2500.0}


if __name__ == "__main__":
    expense = with_retry(fetch_expense_from_dependency)
    print(expense)
