# Day 85 — Bottleneck Analysis

## Objective

Improve capstone performance through measurement, explicit bottleneck hypotheses, and reversible changes. Do not optimize based on intuition alone.

## Investigation workflow

1. **Define the symptom:** identify the endpoint, workload, time window, and user impact.
2. **Measure a baseline:** capture throughput, p50/p95/p99 latency, error rate, CPU, memory, database time, and cache hit ratio.
3. **Trace the request path:** separate application processing, network, database, and downstream-service latency.
4. **Find the limiting resource:** distinguish CPU saturation, I/O waits, lock contention, connection-pool exhaustion, slow queries, and repeated work.
5. **Form one hypothesis:** predict which metric should change if the hypothesis is correct.
6. **Change one variable:** use a representative load test and compare against the baseline.
7. **Verify correctness and rollback:** test stale-data behavior, failure modes, and resource usage before keeping the change.

## Caching decision checklist

- Is the data read frequently and expensive to compute or fetch?
- Can the application tolerate a defined staleness window?
- What is the cache key, TTL, invalidation trigger, and maximum size?
- Could a cache miss or expiry cause a thundering herd?
- What happens when Redis is slow or unavailable?
- Are sensitive or user-specific values isolated by authorization-aware keys?
- Are hit ratio, eviction, latency, and backend load observable?

## Common trade-offs

| Option | Helps when | Risks / costs |
|---|---|---|
| Query/index tuning | Database work dominates | Extra indexes increase write and storage costs |
| Redis cache-aside | Repeated reads tolerate bounded staleness | Invalidation complexity and cache outages |
| Batching | Per-call overhead is high | Larger batches can increase latency and memory use |
| Concurrency | Work waits on independent I/O | Can overload dependencies if unbounded |
| Pagination | Responses or scans are too large | Ordering and cursor semantics need care |

## Acceptance criteria

- [ ] Baseline and test workload are documented.
- [ ] The bottleneck is supported by measurements or traces.
- [ ] Before/after results use the same workload and environment.
- [ ] Cache TTL, invalidation, failure behavior, and metrics are documented.
- [ ] No performance claim is made without recorded evidence.
