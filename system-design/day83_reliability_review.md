# Day 83 — System Design Reliability Review

## Reliability objectives

Define user-visible reliability targets before choosing infrastructure.

- **Availability:** proportion of valid requests that succeed.
- **Latency:** track p50, p95, and p99 rather than relying only on averages.
- **Error rate:** separate expected client errors from server failures.
- **Durability:** define acceptable data-loss windows and recovery objectives.

## Failure analysis

For each critical dependency, document:

| Dependency | Failure symptom | Detection | Mitigation |
|---|---|---|---|
| Primary database | Requests fail or time out | Connection and query metrics | Bounded retries, connection pool limits, recovery procedure |
| Cache | Increased latency or database load | Hit ratio, latency, error metrics | Timeouts, fallback policy, load shedding |
| Background worker | Queue age increases | Queue depth and oldest-message age | Retry policy, dead-letter queue, worker scaling |
| External API | Timeouts or elevated errors | Dependency latency and error rate | Circuit breaker, timeout, bounded retry |

## Resilience patterns

- Set explicit connection and request timeouts.
- Retry only transient failures, with exponential backoff and jitter.
- Avoid retrying non-idempotent writes unless idempotency is guaranteed.
- Use circuit breakers to stop repeatedly calling an unhealthy dependency.
- Use bulkheads and bounded queues to prevent one dependency from exhausting all capacity.
- Apply graceful degradation when an optional dependency is unavailable.
- Keep health checks meaningful: liveness indicates the process is alive; readiness indicates it can safely receive traffic.

## Observability

Every critical request should have a correlation/request ID and structured completion event.
Track request volume, error rate, and latency, plus dependency-specific signals.
Avoid logging credentials, tokens, personal data, or full sensitive request bodies.

## Interview exercise

Design a task-management API that must remain usable during a cache outage.

1. State assumptions and reliability targets.
2. Identify the cache's role and whether it is optional.
3. Define timeouts, fallback behavior, and database protection.
4. Explain how you prevent retry storms and cache stampedes.
5. Describe dashboards, alerts, and a recovery runbook.

## Review checklist

- [ ] SLOs and error-budget implications are explicit.
- [ ] Timeouts and retry budgets are bounded.
- [ ] Writes are idempotent or protected against duplicate execution.
- [ ] Dependency failures are observable.
- [ ] Recovery and degraded-mode behavior are documented.
