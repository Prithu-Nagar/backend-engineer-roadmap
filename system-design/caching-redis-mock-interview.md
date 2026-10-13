# Caching and Redis — Mock System Design Interview

Use this artifact for a 35–45 minute mock interview. State assumptions explicitly and discuss cache correctness, failure behavior, and operational trade-offs.

## 1. Clarify Requirements

Functional requirements:
- Reduce read latency and database load for frequently accessed data.
- Support expiry and an invalidation strategy when source data changes.
- Define which data may be cached and the acceptable staleness window.

Non-functional requirements:
- Keep cache operations low-latency and bound memory use.
- Prevent cache failures from taking down the source database.
- Protect sensitive data and make hit rate, latency, and failures observable.

Clarify read/write ratio, object size, access skew, freshness requirements, and whether cached data may be shared across users or tenants.

## 2. Sketch the Architecture

A common cache-aside read path:

1. The API validates and authorizes the request.
2. The service builds a versioned cache key from trusted identifiers.
3. Redis is queried; a hit returns the cached representation.
4. On a miss, the service reads the authoritative database.
5. The result is cached with a bounded TTL and returned.
6. Metrics record hit/miss, latency, errors, and database fallback behavior.

The database remains the source of truth unless the product explicitly designs otherwise.

## 3. Choose a Caching Pattern

- **Cache-aside:** application loads on miss; flexible, but requires explicit invalidation.
- **Read-through:** cache layer coordinates loading; can simplify callers.
- **Write-through:** update cache and source in a coordinated write path; consistency and failure semantics must be explicit.
- **Write-behind:** writes are deferred; requires durable buffering and clear data-loss/recovery guarantees.

Explain why the selected pattern fits the workload rather than presenting one as universally best.

## 4. Keys, TTL, and Invalidation

- Use namespaced, versioned keys such as `user:v2:{user_id}:profile`.
- Include tenant or authorization scope when cached values are not globally shareable.
- Choose TTL from freshness requirements and refresh cost; jitter expirations to reduce synchronized expiry.
- Invalidate or update affected keys after committed writes; consider versioned keys, event-driven invalidation, or short TTLs.
- Never assume deleting a cache key and committing a database transaction are one atomic operation.

## 5. Failure Modes and Protection

- **Cache stampede:** coalesce concurrent misses, use short-lived locks carefully, add TTL jitter, or refresh popular keys before expiry.
- **Cache penetration:** validate input and consider bounded negative caching for confirmed missing records.
- **Hot keys:** replicate/read-scale where supported, shard carefully, or cache derived aggregates.
- **Redis outage:** use timeouts, circuit breakers, and bounded fallback; protect the database from a surge of misses.
- **Eviction/memory pressure:** set memory limits, select an eviction policy, monitor evictions, and avoid unbounded values.
- **Stale data:** document the consistency contract and the recovery path after failed invalidation.

Choose fail-open or fail-closed based on the endpoint's security and correctness requirements.

## 6. Redis Considerations

Discuss suitable structures such as strings for serialized values, hashes for field-oriented records, sorted sets for ranked/time-based data, and sets for membership. Select structures from access patterns, expiry needs, atomicity requirements, and memory cost. Redis is not a replacement for a durable relational database when transactional relational guarantees are required.

## 7. Observability and Security

Track cache hit ratio, miss rate, p50/p95/p99 latency, Redis timeouts, evictions, memory use, connection saturation, database fallback QPS, and stale-data incidents. Do not place secrets or sensitive data in keys or logs. Restrict network access and credentials, and consider TLS and ACLs.

## 8. Follow-up Questions

1. How would you cache a user profile that changes infrequently?
2. How would you avoid a thundering herd for a popular key?
3. What happens when Redis is unavailable for five minutes?
4. How do you prevent cross-tenant cache leakage?
5. When is caching harmful or unnecessary?
6. How would you invalidate cached data across multiple service instances?
7. Which metric would tell you that the cache is not protecting the database?

## Evaluation Checklist

- [ ] Requirements and freshness contract were clarified.
- [ ] Read and write paths were traced end to end.
- [ ] Key design, TTL, and invalidation were explained.
- [ ] Stampede, outage, eviction, and stale-data behavior were covered.
- [ ] Database overload protection and security were addressed.
- [ ] Metrics and trade-offs were concrete and workload-dependent.
