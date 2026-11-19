import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from token_bucket import TokenBucketRateLimiter


class FakeClock:
    def __init__(self, value=0.0):
        self.value = value

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


def test_bucket_allows_initial_capacity_then_rejects_with_retry_time():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(2, 0.5, clock)

    assert limiter.allow("client").allowed
    assert limiter.allow("client").allowed
    rejected = limiter.allow("client")

    assert not rejected.allowed
    assert rejected.remaining == 0
    assert rejected.retry_after == 2


def test_refill_is_fractional_and_retry_after_tracks_remaining_deficit():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(2, 2, clock)
    limiter.allow("client")
    limiter.allow("client")

    clock.advance(0.25)
    rejected = limiter.allow("client")
    assert not rejected.allowed
    assert rejected.remaining == pytest.approx(0.5)
    assert rejected.retry_after == pytest.approx(0.25)

    clock.advance(0.25)
    allowed = limiter.allow("client")
    assert allowed.allowed
    assert allowed.remaining == 0


def test_refill_never_exceeds_capacity():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(3, 1, clock)
    limiter.allow("client")
    clock.advance(100)

    assert limiter.allow("client", cost=3).allowed
    assert limiter.allow("client").retry_after == 1


def test_buckets_are_independent_by_key():
    limiter = TokenBucketRateLimiter(1, 1, FakeClock())
    assert limiter.allow("first").allowed
    assert not limiter.allow("first").allowed
    assert limiter.allow("second").allowed


def test_clock_moving_backwards_does_not_refill_bucket():
    clock = FakeClock(10)
    limiter = TokenBucketRateLimiter(1, 1, clock)
    limiter.allow("client")
    clock.value = 5

    assert not limiter.allow("client").allowed
    clock.value = 11
    assert limiter.allow("client").allowed


def test_custom_cost_and_reset():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(3, 1, clock)
    decision = limiter.allow("client", cost=2)
    assert decision.allowed and decision.remaining == 1
    limiter.reset("client")
    assert limiter.allow("client", cost=3).allowed
    limiter.reset()
    assert limiter.allow("client", cost=3).allowed


def test_concurrent_requests_cannot_overdraw_a_bucket():
    limiter = TokenBucketRateLimiter(1, 1, FakeClock())
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(lambda _: limiter.allow("shared").allowed, range(100)))
    assert sum(results) == 1


@pytest.mark.parametrize("capacity, refill_rate", [(0, 1), (-1, 1), (1, 0), (1, float("inf"))])
def test_invalid_policy_is_rejected(capacity, refill_rate):
    with pytest.raises((TypeError, ValueError)):
        TokenBucketRateLimiter(capacity, refill_rate)


def test_invalid_key_cost_and_clock_are_rejected():
    limiter = TokenBucketRateLimiter(2, 1, FakeClock())
    with pytest.raises(ValueError, match="key"):
        limiter.allow(" ")
    with pytest.raises(ValueError, match="cost"):
        limiter.allow("client", cost=3)
    with pytest.raises(ValueError, match="cost"):
        limiter.allow("client", cost=0)
    with pytest.raises(ValueError, match="clock"):
        TokenBucketRateLimiter(2, 1, lambda: float("nan")).allow("client")
