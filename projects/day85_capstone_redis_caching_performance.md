# Day 85 — Capstone: Redis Caching and Performance

## Sprint objective

Identify a measurable capstone bottleneck and add caching or query improvements only where evidence supports the change. Preserve existing application behavior and database correctness.

## Implementation plan

1. Select one read-heavy endpoint or repeated database query.
2. Record a baseline with representative request volume, p95 latency, database query count/time, and error rate.
3. Inspect the query plan and add or adjust an index only if the plan and workload justify it.
4. If appropriate, implement Redis cache-aside with a namespaced key, explicit TTL, and serialization validation.
5. Invalidate or refresh the cache after successful source-of-truth writes; document the consistency window.
6. Define behavior for Redis timeout/unavailability, cache misses, and malformed cached values.
7. Add tests for hit, miss, expiry, invalidation, and fallback behavior.
8. Compare before/after measurements under the same workload and record trade-offs.

## Safety and correctness

- The database remains the source of truth.
- Never use a cache key that omits tenant/user scope when data is access-controlled.
- Do not cache secrets or sensitive responses by default.
- Use bounded timeouts and avoid unbounded retry loops.
- Avoid cache stampedes with suitable request coalescing or jitter where needed.
- Keep Redis credentials in runtime configuration and restrict network access.
- Do not claim Redis is integrated unless the real capstone application uses it and tests verify the integration.

## Acceptance criteria

- [ ] The target endpoint/query and baseline metrics are documented.
- [ ] The optimization is tied to an observed bottleneck.
- [ ] TTL, cache key design, invalidation, and failure behavior are documented.
- [ ] Tests cover hit/miss, expiry, invalidation, and dependency failure as applicable.
- [ ] Before/after results and environment are recorded honestly.
- [ ] Existing tests and API contracts remain intact.

## Deliverable

Add a short performance note to the capstone README with the measured baseline, change made, measured result, and known limitations. If no trustworthy measurement is available, document the proposed experiment rather than inventing results.
