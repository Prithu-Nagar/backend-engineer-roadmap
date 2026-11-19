"""Run a deterministic token-bucket demonstration."""

from token_bucket import TokenBucketRateLimiter


class DemoClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def main() -> None:
    clock = DemoClock()
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate=1, clock=clock)

    for request_number in range(1, 5):
        decision = limiter.allow("demo-client")
        status = "allowed" if decision.allowed else "rejected"
        print(
            f"Request {request_number}: {status}; "
            f"remaining={decision.remaining:.2f}; "
            f"retry_after={decision.retry_after:.2f}s"
        )

    clock.advance(1)
    decision = limiter.allow("demo-client")
    print(f"After one second: {'allowed' if decision.allowed else 'rejected'}")


if __name__ == "__main__":
    main()
