"""Redis-backed, atomic token-bucket rate limiter."""

from __future__ import annotations

import math
from typing import Any

from token_bucket import RateLimitDecision

_TOKEN_BUCKET_SCRIPT = """
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])
local ttl_ms = tonumber(ARGV[4])

local time_parts = redis.call('TIME')
local now = tonumber(time_parts[1]) + tonumber(time_parts[2]) / 1000000

local values = redis.call('HMGET', KEYS[1], 'tokens', 'updated_at')
local tokens = tonumber(values[1])
local updated_at = tonumber(values[2])

if (values[1] and not tokens) or (values[2] and not updated_at) then
    return redis.error_reply('invalid token bucket state')
end
if (values[1] == false) ~= (values[2] == false) then
    return redis.error_reply('incomplete token bucket state')
end

if not tokens or not updated_at then
    tokens = capacity
    updated_at = now
else
    local elapsed = math.max(0, now - updated_at)
    tokens = math.min(capacity, tokens + elapsed * refill_rate)
    updated_at = math.max(now, updated_at)
end

local allowed = 0
local retry_after = 0
if tokens >= cost then
    tokens = tokens - cost
    allowed = 1
else
    retry_after = (cost - tokens) / refill_rate
end

redis.call('HSET', KEYS[1], 'tokens', tokens, 'updated_at', updated_at)
redis.call('PEXPIRE', KEYS[1], ttl_ms)

return {allowed, tokens, retry_after}
"""


class RedisTokenBucketRateLimiter:
    """Token bucket whose state and decisions are shared through Redis.

    Redis executes each decision as one Lua script, so separate application
    instances cannot race between reading and updating the same bucket.
    Redis server time is authoritative; application-host clocks are not used.
    """

    def __init__(
        self,
        redis_client: Any,
        capacity: float,
        refill_rate: float,
        key_prefix: str = "rate-limit",
    ) -> None:
        self._validate_positive_finite("capacity", capacity)
        self._validate_positive_finite("refill_rate", refill_rate)
        if not callable(getattr(redis_client, "eval", None)):
            raise TypeError("redis_client must provide an eval method")
        if not isinstance(key_prefix, str) or not key_prefix.strip():
            raise ValueError("key_prefix must be a non-empty string")

        self.client = redis_client
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.key_prefix = key_prefix.rstrip(":")
        # An idle bucket expires once it would have naturally refilled fully.
        self.ttl_ms = max(1, math.ceil(self.capacity / self.refill_rate * 1000))

    @staticmethod
    def _validate_positive_finite(name: str, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be positive and finite")

    def allow(self, key: str, cost: float = 1) -> RateLimitDecision:
        """Atomically consume tokens for ``key`` using Redis server time."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("key must be a non-empty string")
        self._validate_positive_finite("cost", cost)
        if cost > self.capacity:
            raise ValueError("cost cannot exceed bucket capacity")

        redis_key = f"{self.key_prefix}:{key}"
        result = self.client.eval(
            _TOKEN_BUCKET_SCRIPT,
            1,
            redis_key,
            self.capacity,
            self.refill_rate,
            float(cost),
            self.ttl_ms,
        )
        if not isinstance(result, (list, tuple)) or len(result) != 3:
            raise RuntimeError("Redis rate limiter returned an invalid response")

        allowed, remaining, retry_after = result
        return RateLimitDecision(
            bool(int(allowed)),
            self.capacity,
            float(remaining),
            float(retry_after),
        )
