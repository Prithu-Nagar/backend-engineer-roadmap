# Circuit Breakers & Bulkheads

Day 39 introduces two resilience patterns for preventing one failing
Dependency from consuming all of a service's capacity.

## Circuit Breaker

A circuit breaker watches failures from a downstream dependency and changes
how calls are handled when the dependency becomes unhealthy.

### States

```text
                 failure threshold reached
        +--------------------------------------+
        |                                      v
     CLOSED ------------------------------> OPEN
        ^                                      |
        |                                      | wait / timeout
        |                                      v
        +------------- success ------------ HALF-OPEN
                                               |
                                               +--> failure -> OPEN
```

- **Closed** — calls flow normally and failures are counted.
- **Open** — calls fail fast without contacting the dependency.
- **Half-open** — a limited probe checks whether recovery has occurred.

A circuit breaker should use a bounded observation window and a clear recovery
policy rather than remaining open forever.

## Why Fail Fast?

If a dependency is timing out, allowing every request to wait for that timeout
can exhaust worker threads, connection pools, queues, and request deadlines.
Failing fast preserves capacity for work that can still succeed.

## Bulkheads

A bulkhead isolates resource pools so one workload cannot consume all available
capacity.

```text
                 Service
                    |
          +---------+---------+
          |                   |
      Expense API         Reporting API
          |                   |
      Pool A              Pool B
          |                   |
      Dependency X       Dependency Y
```

Examples include:

- Separate worker pools for unrelated workloads
- Independent connection pools
- Per-tenant concurrency limits
- Dedicated queues for high-priority work

The goal is containment: failure or overload in one area should not exhaust the
resources required by another area.

## Circuit Breaker vs Bulkhead

| Pattern | Primary goal | Typical control |
|---|---|---|
| Circuit breaker | Stop calls to an unhealthy dependency | Failure threshold + open state |
| Bulkhead | Isolate resource consumption | Separate pools/queues/limits |

They are complementary. A service can use bulkheads to limit concurrency and a
circuit breaker to stop calls when the dependency is clearly unhealthy.

## Interaction with Retries

Retries and circuit breakers must be designed together.

```text
request
  |
  v
bulkhead admission
  |
  v
circuit breaker
  |  | open -> fail fast
  v
attempt dependency call
  |
  v
bounded retry policy
```

A retry policy should remain bounded by attempts and deadlines. If the circuit
is open, retries should not bypass it and recreate the same load problem.

## Practical Signals

Useful metrics include:

- Circuit state changes
- Calls rejected by an open circuit
- Dependency failure rate
- Dependency latency
- Bulkhead queue depth
- Active and rejected work
- Retry count
- Request deadline exhaustion

These signals help distinguish dependency failure from local capacity
exhaustion.

## Interview Questions

1. What problem does a circuit breaker solve?
2. Why are closed, open, and half-open states useful?
3. How does a bulkhead prevent cascading failures?
4. When would you isolate worker pools or connection pools?
5. Why should retries not bypass an open circuit?
6. How do deadlines interact with circuit breakers and retries?
7. Which metrics would you monitor to verify the design?
