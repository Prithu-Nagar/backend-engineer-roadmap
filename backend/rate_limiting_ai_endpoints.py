"""
Day 59 — Rate Limiting AI Endpoints

Provider-neutral token-bucket rate limiting for expensive AI-backed endpoints.
The limiter is intentionally independent of Flask/FastAPI/Django so the
policy can be reused at the service boundary or behind an API gateway.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass
class Bucket:
    tokens: float
    last_refill: float


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_per_second: float) -> None:
        if capacity <= 0 or refill_per_second <= 0:
            raise ValueError("capacity and refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_per_second = refill_per_second
        self.buckets: dict[str, Bucket] = {}

    def allow(self, key: str, *, cost: float = 1.0) -> bool:
        """Consume request capacity if the caller has enough tokens."""
        if cost <= 0 or cost > self.capacity:
            raise ValueError("cost must be greater than zero and within capacity")

        now = monotonic()
        bucket = self.buckets.get(key)

        if bucket is None:
            bucket = Bucket(self.capacity, now)
            self.buckets[key] = bucket

        elapsed = now - bucket.last_refill
        bucket.tokens = min(
            self.capacity,
            bucket.tokens + elapsed * self.refill_per_second,
        )
        bucket.last_refill = now

        if bucket.tokens < cost:
            return False

        bucket.tokens -= cost
        return True


def ai_request_cost(*, estimated_input_tokens: int, priority: str) -> float:
    """Assign more quota cost to expensive requests."""
    base_cost = max(1.0, estimated_input_tokens / 1_000)

    if priority == "batch":
        return base_cost * 0.5
    if priority == "high":
        return base_cost * 2

    return base_cost


if __name__ == "__main__":
    limiter = TokenBucketRateLimiter(capacity=10, refill_per_second=2)

    request_cost = ai_request_cost(
        estimated_input_tokens=2_000,
        priority="standard",
    )

    print(limiter.allow("tenant-42", cost=request_cost))
