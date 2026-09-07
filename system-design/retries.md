# Retries, Exponential Backoff & Jitter

Day 38 introduces retry strategies for transient failures in distributed
services.

## Why Retries Exist

Network calls and shared dependencies can fail temporarily because of:

- Connection timeouts
- Short-lived network failures
- Temporary dependency overload
- Leader elections or failovers
- Rate limiting

A retry can turn a transient failure into a successful request, but an
uncontrolled retry policy can amplify an outage.

## Retry Only When Appropriate

A request should be retried only when the failure is plausibly transient and
the operation is safe to repeat.

Good candidates often include:

- Idempotent reads
- Idempotent writes with an idempotency key
- Explicitly retryable dependency failures

Avoid blind retries for operations where repeating the action can create
additional side effects.

## Exponential Backoff

Instead of retrying immediately, increase the delay after each failed attempt.

```text
base delay = 100 ms
attempt 1 -> 100 ms
attempt 2 -> 200 ms
attempt 3 -> 400 ms
attempt 4 -> 800 ms
```

A common capped formula is:

```text
delay = min(max_delay, base_delay * 2^attempt)
```

The cap prevents an individual request from waiting indefinitely.

## Jitter

If thousands of clients fail at the same time and all retry on the same fixed
schedule, they can overload the dependency again.

Jitter randomizes the delay:

```text
sleep = random(0, calculated_backoff)
```

This spreads retries over time and reduces synchronized retry bursts.

## Retry Budget

A production policy should bound the total work spent retrying.

Typical controls include:

- Maximum attempts
- Maximum elapsed retry time
- Maximum backoff delay
- Per-request deadline
- Per-service retry budget

The deadline should include the original attempt and all retry attempts.

## Respect Dependency Signals

A dependency may communicate that the caller should slow down. HTTP clients
should honor `Retry-After` when appropriate instead of immediately applying a
local retry schedule.

Retries should also distinguish:

- Timeout
- Connection failure
- Rate limiting
- Server-side 5xx failure
- Client-side 4xx failure

Most ordinary validation and authorization failures should not be retried.

## Retry Storms

Consider a dependency that becomes unavailable:

```text
Clients
 |  |  |  |
 |  |  |  |
 +--+--+--+
      |
      v
   Service A
      |
      v
  Dependency X  <- overloaded
```

If every failed request immediately retries, Service A creates even more load
against Dependency X. Backoff, jitter, deadlines, circuit breakers, and bounded
retry budgets reduce this feedback loop.

## Idempotency

Retries are safest when the operation has a stable outcome under repetition.

For a write operation, an idempotency key can allow the service to recognize a
repeated request instead of creating duplicate state.

```text
Client
  |
  | idempotency-key=req-1001
  v
Service
  |
  +--> process once
  |
  +--> store result
  |
  +--> return stored result for duplicate request
```

## Recommended Policy Shape

```text
request
  |
  v
is failure retryable?
  | no ----------------------> return failure
  |
 yes
  |
  v
is operation safe to repeat?
  | no ----------------------> return failure
  |
 yes
  |
  v
within deadline / retry budget?
  | no ----------------------> return failure
  |
 yes
  |
  v
exponential backoff + jitter
  |
  v
retry
```

## Interview Questions

1. Why is exponential backoff preferable to immediate retries?
2. What problem does jitter solve?
3. Which HTTP failures should normally not be retried?
4. How does idempotency make write retries safer?
5. How can retries make an outage worse?
6. What should a retry budget contain?
7. When should a client honor `Retry-After`?
