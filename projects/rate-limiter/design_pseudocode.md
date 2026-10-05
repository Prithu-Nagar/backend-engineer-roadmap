# Rate Limiter — Design and Pseudocode

## Day 66

This document converts the Rate Limiter HLD into a compact design artifact that
can be explained during an interview and later mapped to a backend
implementation.

---

## 1. Design

```text
Client
  |
  v
API Gateway / Backend
  |
  +--> authenticate request
  |
  +--> derive rate-limit key
  |
  +--> load policy
  |
  +--> atomic token-bucket decision
          |
          +--> allowed --> handler
          |
          +--> rejected --> HTTP 429
```

Example key:

```text
rate:{policy_id}:{tenant_id}:{user_id}:{route_group}
```

Only the dimensions required by the policy should be included. Avoid creating
high-cardinality keys without an operational reason.

---

## 2. Token-Bucket Pseudocode

```text
function allow_request(key, policy, now):
    state = store.get(key)

    if state does not exist:
        tokens = policy.capacity
        last_refill = now
    else:
        tokens = state.tokens
        last_refill = state.last_refill

    elapsed = max(0, now - last_refill)
    refilled = min(
        policy.capacity,
        tokens + elapsed * policy.refill_rate,
    )

    if refilled < policy.request_cost:
        retry_after = seconds_until_next_token(
            policy.request_cost - refilled,
            policy.refill_rate,
        )
        store.save(
            key,
            tokens=refilled,
            last_refill=now,
            ttl=policy.expiry,
        )
        return REJECT, retry_after

    remaining = refilled - policy.request_cost
    store.save(
        key,
        tokens=remaining,
        last_refill=now,
        ttl=policy.expiry,
    )
    return ALLOW, remaining
```

The read-modify-write sequence must execute atomically in the shared store.
The pseudocode is therefore a logical algorithm, not an instruction to issue
separate non-atomic Redis commands.

---

## 3. Atomic Redis-Style Pseudocode

```text
EVAL rate_limit_script KEYS[1] ARGV[
    capacity,
    refill_rate,
    request_cost,
    now,
    ttl
]

script:
    state = HGETALL key
    calculate refilled tokens

    if refilled < request_cost:
        HSET key tokens=refilled last_refill=now
        EXPIRE key ttl
        return [0, retry_after, refilled]

    HSET key tokens=(refilled - request_cost) last_refill=now
    EXPIRE key ttl
    return [1, 0, refilled - request_cost]
```

A real implementation should validate numeric inputs, handle malformed state,
and define how policy changes interact with existing counters.

---

## 4. HTTP Contract

Allowed request:

```http
200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
```

Rejected request:

```http
429 Too Many Requests
Retry-After: 2
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
```

The exact header contract should be standardized across the API rather than
implemented differently by individual endpoints.

---

## 5. Failure Policy

The project should make the dependency failure policy explicit:

```text
if limiter_store_unavailable:
    if endpoint_policy == "availability_first":
        allow_with_metric("rate_limiter_fail_open")
    else:
        reject_with_503("rate_limiter_unavailable")
```

A security-sensitive operation may require stricter protection than a normal
read API. The policy should be configurable and observable.

---

## 6. Interview Explanation

Explain the design in this order:

1. Define the business requirement and scope.
2. Choose token bucket and explain burst behavior.
3. Derive a deterministic rate-limit key.
4. Store shared counters in Redis for horizontally scaled services.
5. Make the counter update atomic.
6. Return remaining capacity and retry information.
7. Explain Redis failure, hot keys, and clock behavior.
8. Estimate active keys and decision throughput.
9. Add metrics for allowed, rejected, latency, and dependency failures.
10. Discuss regional versus global quota semantics.

The central design principle is that rate-limit state is a shared concurrency
boundary, so the decision must remain atomic even when requests are distributed
across many backend instances.
