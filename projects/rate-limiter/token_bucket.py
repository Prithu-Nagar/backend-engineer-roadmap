"""Thread-safe in-process token-bucket rate limiter."""

from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitDecision:
    """Result of one token-bucket decision."""

    allowed: bool
    limit: float
    remaining: float
    retry_after: float


@dataclass
class _BucketState:
    tokens: float
    updated_at: float


class TokenBucketRateLimiter:
    """A process-local token bucket with an injectable monotonic clock.

    The lock makes each read/refill/consume operation atomic between threads in
    this process. State is not shared between processes or application hosts.
    """

    def __init__(
        self,
        capacity: float,
        refill_rate: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._validate_positive_finite("capacity", capacity)
        self._validate_positive_finite("refill_rate", refill_rate)
        if not callable(clock):
            raise TypeError("clock must be callable")
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._clock = clock
        self._buckets: dict[str, _BucketState] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _validate_positive_finite(name: str, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be positive and finite")

    def allow(self, key: str, cost: float = 1) -> RateLimitDecision:
        """Consume ``cost`` tokens for ``key`` when sufficient capacity exists."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("key must be a non-empty string")
        self._validate_positive_finite("cost", cost)
        if cost > self.capacity:
            raise ValueError("cost cannot exceed bucket capacity")

        now = float(self._clock())
        if not math.isfinite(now):
            raise ValueError("clock must return a finite timestamp")

        with self._lock:
            state = self._buckets.get(key)
            if state is None:
                tokens = self.capacity
                updated_at = now
            else:
                # A clock that moves backwards must not create extra tokens.
                updated_at = max(now, state.updated_at)
                elapsed = updated_at - state.updated_at
                tokens = min(
                    self.capacity,
                    state.tokens + elapsed * self.refill_rate,
                )

            if tokens >= cost:
                remaining = tokens - cost
                self._buckets[key] = _BucketState(remaining, updated_at)
                return RateLimitDecision(True, self.capacity, remaining, 0.0)

            deficit = cost - tokens
            retry_after = deficit / self.refill_rate
            self._buckets[key] = _BucketState(tokens, updated_at)
            return RateLimitDecision(False, self.capacity, tokens, retry_after)

    def reset(self, key: str | None = None) -> None:
        """Reset one bucket, or all buckets when ``key`` is omitted."""
        with self._lock:
            if key is None:
                self._buckets.clear()
            else:
                self._buckets.pop(key, None)
