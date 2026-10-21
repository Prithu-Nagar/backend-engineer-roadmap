# Day 82 — Scalability Review

Use this checklist to review a backend design under increasing traffic and
data volume. Base recommendations on workload assumptions or measurements.

## 1. Establish the workload

- Peak and average requests per second:
- Read/write ratio and request-size distribution:
- Data growth and retention requirements:
- Latency targets (p50, p95, p99):
- Availability target and acceptable data loss:
- Geographic distribution and traffic seasonality:

## 2. Find likely bottlenecks

| Layer | Signals to inspect | Possible response | Trade-off |
|---|---|---|---|
| API workers | Saturation, queueing, p95/p99 latency | Horizontal scale, bounded concurrency | Cost and coordination |
| Database | Slow queries, locks, pool wait time | Query/index tuning, connection pooling, read replicas | Write cost and replica lag |
| Cache | Hit ratio, evictions, stale reads | TTL, invalidation, stampede protection | Consistency complexity |
| Queue/workers | Queue depth, age of oldest item, retry rate | Scale consumers, bound retries | Delayed completion |
| External dependency | Timeout/error rate, latency | Timeouts, circuit breaker, fallback | Partial functionality |

## 3. Capacity estimate

1. Estimate peak request rate rather than using daily averages alone.
2. Estimate work per request, payload sizes, and database queries per request.
3. Estimate concurrency with Little's Law: `in_flight ≈ throughput × latency`.
4. Add headroom for bursts and failure of one instance or dependency.
5. Validate estimates with load tests and production telemetry.

Example only: 500 requests/second at 0.2 seconds average latency implies
roughly 100 requests in flight. This is an estimate, not a sizing guarantee.

## 4. Scale deliberately

- Prefer stateless API instances where practical; externalize shared session state.
- Add caching only after defining freshness and invalidation requirements.
- Use asynchronous jobs for work that need not complete in the request path.
- Keep database transactions short and connection pools bounded.
- Use backpressure, timeouts, bounded retries, and idempotency for failure control.
- Consider partitioning or sharding only when simpler approaches are insufficient.

## 5. Reliability and verification

- [ ] Identify single points of failure and dependency failure modes.
- [ ] Define health checks, readiness, graceful shutdown, and overload behavior.
- [ ] Track request rate, errors, latency, saturation, queue age, and DB pool wait.
- [ ] Load-test representative traffic and document test limits.
- [ ] Record the bottleneck, evidence, chosen change, alternative, and trade-off.

## Interview prompt

Design a service expected to grow from 100 to 5,000 requests/second. Ask for
missing requirements first, estimate capacity, identify the first bottleneck,
propose an incremental scaling plan, and explain consistency and operational
trade-offs.
