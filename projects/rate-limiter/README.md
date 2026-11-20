# Rate Limiter Project

## In-process token bucket

The project now includes a runnable, thread-safe in-process token-bucket
implementation in `token_bucket.py`.

- Configurable bucket capacity and refill rate (tokens per second).
- Injectable clock for deterministic tests and reproducible behavior.
- Per-key buckets with independent state.
- Atomic read/refill/consume decisions between threads in one process.
- Remaining-token and retry-after values in every decision.
- Input validation and explicit reset support.

Run the demo from the repository root:

```bash
python projects/rate-limiter/demo.py
```

Run the focused tests:

```bash
python -m pytest projects/rate-limiter/tests -q
```

The implementation is process-local. Separate workers or hosts do not share
bucket state; the Redis-backed atomic variant, TTL behavior, and distributed
concurrency assumptions are the next milestone. The existing design document
retains the shared-store and failure-policy architecture for that extension.

## Design reference

`design_pseudocode.md` describes the intended Redis-backed atomic design,
HTTP response contract, failure policy, and operational trade-offs. The
pseudocode is not presented as a completed Redis integration.


## Redis-backed token bucket

`redis_token_bucket.py` adds a shared-state implementation for deployments
running multiple application workers or hosts. It accepts a configured
`redis.Redis` client (the `redis` package is already pinned in
`python/requirements.txt`):

```python
import redis

from redis_token_bucket import RedisTokenBucketRateLimiter

client = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=False)
limiter = RedisTokenBucketRateLimiter(
    client,
    capacity=100,
    refill_rate=10,
    key_prefix="my-api:rate-limit",
)

decision = limiter.allow("user:123")
```

Each decision runs as one Redis Lua script. The script reads and updates the
bucket atomically and uses Redis server time, so application-host clock skew
does not affect shared decisions. The key expires after an idle period equal
to the time required to refill a completely empty bucket. Expiration is
refreshed on each decision.

All application instances must use the same Redis deployment, compatible
policy values, and the same key prefix/key derivation to share a quota.
Different prefixes or Redis databases create independent limits. Redis
availability is a runtime dependency; callers must choose and implement their
own fail-open or fail-closed policy. This adapter does not provide a Flask
middleware, metrics, or a Redis connection lifecycle manager.

The Redis tests use an atomic in-memory test double to verify adapter behavior,
TTL calculation, shared-instance limits, and concurrency. They do not replace
an integration test against a live Redis server.
