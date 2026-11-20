"""Tests for the Redis token bucket using an atomic in-memory Redis double."""

import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from redis_token_bucket import RedisTokenBucketRateLimiter


class FakeRedis:
    """Small deterministic stand-in for the Redis commands used by the script."""

    def __init__(self):
        self.now = 100.0
        self.data = {}
        self.lock = threading.Lock()
        self.last_ttl_ms = None

    def eval(self, script, number_of_keys, key, capacity, refill_rate, cost, ttl_ms):
        assert number_of_keys == 1
        assert "redis.call('TIME')" in script
        assert "redis.call('PEXPIRE'" in script
        with self.lock:
            record = self.data.get(key)
            if record and record["expires_at"] <= self.now:
                del self.data[key]
                record = None

            if record is None:
                tokens = float(capacity)
                updated_at = self.now
            else:
                elapsed = max(0.0, self.now - record["updated_at"])
                tokens = min(float(capacity), record["tokens"] + elapsed * float(refill_rate))
                updated_at = max(self.now, record["updated_at"])

            allowed = int(tokens >= float(cost))
            retry_after = 0.0
            if allowed:
                tokens -= float(cost)
            else:
                retry_after = (float(cost) - tokens) / float(refill_rate)

            self.data[key] = {
                "tokens": tokens,
                "updated_at": updated_at,
                "expires_at": self.now + int(ttl_ms) / 1000,
            }
            self.last_ttl_ms = int(ttl_ms)
            return [allowed, tokens, retry_after]

    def advance(self, seconds):
        self.now += seconds


@pytest.fixture
def redis_client():
    return FakeRedis()


def test_shared_bucket_enforces_limit_and_reports_retry(redis_client):
    limiter = RedisTokenBucketRateLimiter(redis_client, capacity=2, refill_rate=0.5)

    assert limiter.allow("client").allowed
    assert limiter.allow("client").allowed
    rejected = limiter.allow("client")

    assert not rejected.allowed
    assert rejected.remaining == 0
    assert rejected.retry_after == pytest.approx(2)


def test_refill_uses_shared_store_time(redis_client):
    limiter = RedisTokenBucketRateLimiter(redis_client, capacity=1, refill_rate=2)
    assert limiter.allow("client").allowed
    assert not limiter.allow("client").allowed

    redis_client.advance(0.5)
    decision = limiter.allow("client")
    assert decision.allowed
    assert decision.remaining == pytest.approx(0)


def test_ttl_expires_idle_bucket_after_full_refill_period(redis_client):
    limiter = RedisTokenBucketRateLimiter(redis_client, capacity=4, refill_rate=2)
    limiter.allow("client")

    assert redis_client.last_ttl_ms == 2000
    assert "rate-limit:client" in redis_client.data

    redis_client.advance(2.001)
    assert limiter.allow("client", cost=4).allowed


def test_two_instances_share_one_atomic_bucket(redis_client):
    first = RedisTokenBucketRateLimiter(redis_client, capacity=5, refill_rate=1)
    second = RedisTokenBucketRateLimiter(redis_client, capacity=5, refill_rate=1)

    assert first.allow("tenant-user").allowed
    assert second.allow("tenant-user", cost=4).allowed
    assert not first.allow("tenant-user").allowed


def test_concurrent_instances_cannot_overdraw_shared_bucket(redis_client):
    limiters = [
        RedisTokenBucketRateLimiter(redis_client, capacity=10, refill_rate=1)
        for _ in range(4)
    ]

    def request(index):
        return limiters[index % len(limiters)].allow("shared").allowed

    with ThreadPoolExecutor(max_workers=20) as executor:
        decisions = list(executor.map(request, range(100)))

    assert sum(decisions) == 10


def test_keys_are_isolated_and_prefix_is_applied(redis_client):
    limiter = RedisTokenBucketRateLimiter(redis_client, 1, 1, key_prefix="api:v1")
    assert limiter.allow("user-a").allowed
    assert limiter.allow("user-b").allowed
    assert "api:v1:user-a" in redis_client.data
    assert "api:v1:user-b" in redis_client.data


@pytest.mark.parametrize("capacity, refill_rate", [(0, 1), (-1, 1), (1, 0), (1, float("inf"))])
def test_invalid_policy_is_rejected(redis_client, capacity, refill_rate):
    with pytest.raises((TypeError, ValueError)):
        RedisTokenBucketRateLimiter(redis_client, capacity, refill_rate)


def test_invalid_key_cost_and_client_are_rejected(redis_client):
    limiter = RedisTokenBucketRateLimiter(redis_client, 2, 1)
    with pytest.raises(ValueError, match="key"):
        limiter.allow(" ")
    with pytest.raises(ValueError, match="cost"):
        limiter.allow("client", cost=3)
    with pytest.raises(ValueError, match="cost"):
        limiter.allow("client", cost=0)
    with pytest.raises(TypeError, match="eval"):
        RedisTokenBucketRateLimiter(object(), 2, 1)


def test_malformed_redis_response_is_rejected():
    class BadRedis:
        def eval(self, *args):
            return [1]

    limiter = RedisTokenBucketRateLimiter(BadRedis(), 2, 1)
    with pytest.raises(RuntimeError, match="invalid response"):
        limiter.allow("client")
