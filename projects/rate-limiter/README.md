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

## Flask API middleware

`flask_middleware.py` provides a reusable Flask integration for either limiter
implementation. Register it with an application, a limiter instance, and a
trusted identity function:

```python
from flask import Flask
from flask_middleware import register_rate_limit
from token_bucket import TokenBucketRateLimiter

app = Flask(__name__)
limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1)
register_rate_limit(
    app,
    limiter,
    key_func=lambda request: request.headers.get("X-Authenticated-User", "anonymous"),
)
```

The middleware returns HTTP `429` when the quota is exhausted and includes
`Retry-After`, `X-RateLimit-Limit`, and `X-RateLimit-Remaining` headers. Limiter
backend errors fail closed with HTTP `503` by default. Set `fail_open=True`
only when endpoint availability is more important than enforcing the quota;
such responses carry `X-RateLimit-Status: unavailable`. The demo identity
header is for local demonstration only: production applications should derive
the key from authenticated identity and trust forwarded client addresses only
behind a correctly configured proxy.

Run the API example from the repository root:

```bash
python projects/rate-limiter/api_demo.py
```

Then request `http://127.0.0.1:5000/resource`. The example uses the in-process
limiter; replace it with `RedisTokenBucketRateLimiter` and a configured Redis
client to share counters across application instances.

Run all focused tests, including HTTP contract and backend-failure behavior:

```bash
python -m pytest projects/rate-limiter/tests -q
```

The Redis adapter is tested with an atomic in-memory test double. A live Redis
server integration test and production deployment behavior are not claimed.
