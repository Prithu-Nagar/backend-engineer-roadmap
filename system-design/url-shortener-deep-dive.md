# URL Shortener — HLD Deep Dive

## Day 65

Day 65 deepens the URL Shortener HLD from Day 64. The goal is to reason about
how the design behaves as traffic grows, how the redirect path stays fast, and
how ownership, consistency, API evolution, and operational concerns interact.

The design keeps the URL Service as the owner of URL mappings and treats the
User Service as the owner of identity data. Capacity figures are illustrative;
production values should come from measured workload data.

---

## 1. Design Goals

The URL Shortener should:

- Create unique short URLs reliably.
- Redirect quickly on the dominant read path.
- Remain horizontally scalable at the application layer.
- Keep URL and identity data ownership explicit.
- Support API evolution without silently breaking clients.
- Tolerate cache, replica, and individual application-instance failures.
- Provide enough observability to identify the next bottleneck.

Non-goals for the first version:

- Global multi-region active/active writes.
- Arbitrary cross-service transactions.
- Sharding before single-database limits are measured.

---

## 2. Refined Architecture

```text
                         +----------------+
Client ---------------->| API Gateway    |
                         +--------+-------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             +-------------+              +-------------+
             | URL Service |              | User Service |
             +------+------+              +------+------+
                    |                            |
              +-----+-----+                    User DB
              |           |
              v           v
          URL Cache      URL DB
              |
              v
        Redirect response
```

The API Gateway can provide TLS termination, authentication handoff, request
limits, routing, and observability. It should not become the owner of URL
business rules.

---

## 3. Read Path: Redirect

The redirect path is the critical latency path because reads substantially
outnumber URL creations.

```text
Client
  |
  v
Gateway
  |
  v
URL Service
  |
  +--> Cache GET(short_code)
  |       |
  |       +--> HIT --> validate cached state --> redirect
  |
  +--> URL DB lookup
          |
          +--> check active/expiry
          |
          +--> populate cache
          |
          v
       redirect
```

Important decisions:

- The database remains authoritative for URL existence and state.
- Cache entries should have a bounded TTL.
- Expiration state must not be allowed to outlive the business rule silently.
- Cache failure should degrade to a database lookup rather than make the whole
  redirect service unavailable.
- Negative caching can reduce repeated misses, but the TTL must be short enough
  to avoid hiding a newly-created URL.

---

## 4. Write Path: Create URL

```text
Client
  |
  v
Gateway
  |
  v
URL Service
  |
  +--> authenticate / authorize
  |
  +--> validate destination URL
  |
  +--> generate or validate short code
  |
  +--> INSERT mapping
  |
  +--> optional cache write / invalidation
  |
  v
201 Created
```

The database uniqueness constraint is the final authority for a short-code
collision. Application-side checks can improve user experience but cannot
replace the constraint under concurrent writes.

For retried create requests, an idempotency key can map a client operation to a
stable result when the API contract requires exactly-once user-visible behavior.

---

## 5. Capacity and Bottlenecks

The Day 64 assumptions used approximately 1,930 peak redirects/second and
193 peak creates/second. At that scale, the first bottlenecks are more likely to
be connection management, inefficient queries, cache misses, or application
saturation than the need for immediate sharding.

Measure:

- Requests/second by endpoint.
- p50, p95, and p99 latency.
- Cache hit ratio.
- Database CPU and I/O utilization.
- Connection-pool utilization.
- Slow-query frequency.
- Replica lag.
- Error and timeout rates.

A useful capacity rule is to scale from measured saturation rather than a
single theoretical QPS number.

---

## 6. Database Scaling

Start with a relational primary because the URL mapping requires durable
writes and uniqueness guarantees.

### Indexes

The redirect query should have an index beginning with `short_code`.
Metadata queries can use an owner/time access path.

### Read Replicas

Read replicas are useful for workloads that tolerate replica lag, such as
analytics or non-critical metadata reads. The redirect path should define
whether stale reads are acceptable before routing traffic to replicas.

### Partitioning

Partition very large event or analytics tables when partition pruning and
maintenance benefits are measurable. Time is a natural partition key for
append-heavy event history.

### Sharding

Sharding should be a later step. A viable shard key needs to distribute load
while preserving the lookup pattern. Introducing shards also changes routing,
rebalancing, backups, migrations, and operational failure handling.

---

## 7. Cache Strategy

Recommended initial cache value:

```text
key:   url:{short_code}
value: {destination_url, active, expires_at}
TTL:   bounded and workload-specific
```

### Cache Miss

Read from the URL database, then populate the cache.

### Cache Stampede

If a hot key expires, many requests can miss together. Possible mitigations:

- Short randomized TTL jitter.
- Single-flight/request coalescing.
- Temporary locks for expensive recomputation.
- Stale-while-revalidate where business rules permit it.

### Cache Invalidation

On URL deactivation or destination changes, invalidate or update the cached
mapping. TTL remains a safety boundary rather than the only consistency tool.

---

## 8. API Versioning

The backend should avoid silently changing an existing response contract.
Versioning can be introduced through a URL path such as:

```text
/api/v1/urls
/api/v2/urls
```

or through another explicit contract such as a versioned media type.

For the learning implementation, URL-path versioning is easiest to explain:

- Keep `v1` stable during the migration window.
- Introduce `v2` with an explicit contract change.
- Share domain/application logic where possible.
- Version serializers and compatibility behavior at the API boundary.
- Publish a deprecation date before removing an old contract.

API versioning should not require duplicating the entire service. The domain
model and core use cases can remain shared while representation contracts evolve.

---

## 9. Consistency Model

Different operations can have different consistency requirements.

| Operation | Preferred consistency |
|---|---|
| Create URL response | Strong/read-your-write from primary |
| Immediate redirect after create | Read-your-write preferred |
| Analytics counters | Eventual consistency acceptable |
| Cached redirect | Bounded staleness based on TTL/invalidation |
| User profile metadata | Depends on endpoint requirements |

Explicitly defining consistency prevents accidental dependence on a replica or
cache that may be stale.

---

## 10. Failure Modes

| Failure | Handling |
|---|---|
| Cache unavailable | Fall back to database |
| Cache contains expired mapping | Validate expiry before redirect |
| Database replica lag | Route consistency-sensitive reads to primary |
| Primary database unavailable | Fail writes safely; use a documented recovery/failover process |
| Application instance failure | Load balancer routes around unhealthy instance |
| User service unavailable | Redirect should not depend on a live user lookup |
| Short-code collision | Database constraint rejects collision; generate another code |
| Duplicate create request | Idempotency strategy where supported |
| Hot key | Cache + request coalescing / rate controls |

---

## 11. Observability

### Metrics

- Redirect QPS.
- Create QPS.
- Cache hit/miss ratio.
- p95/p99 redirect latency.
- Database query latency.
- Connection-pool utilization.
- Replica lag.
- Error rate by endpoint and status code.
- Short-code collision rate.

### Logs

Include a request/correlation ID and avoid logging sensitive user data or full
Authorization headers.

### Traces

A distributed trace should make it possible to see:

```text
Gateway -> URL Service -> Cache -> URL DB
```

for a slow redirect without requiring manual correlation across unrelated logs.

---

## 12. Evolution Path

A practical sequence is:

1. Single relational primary + indexed mappings.
2. Stateless URL Service behind a load balancer.
3. Cache hot redirect mappings.
4. Add connection pooling and query monitoring.
5. Add read replicas for suitable reads.
6. Partition high-volume event/analytics tables.
7. Introduce asynchronous analytics processing.
8. Revisit sharding only after measured single-database limits are reached.
9. Consider multi-region architecture only when availability/latency
   requirements justify its operational complexity.

This sequence keeps each scaling step tied to an observable bottleneck.

---

## Interview Discussion Points

- Why is the redirect path read-heavy?
- Why is the database uniqueness constraint still required if the application
  checks for an existing short code first?
- When is a cache appropriate, and what happens when it fails?
- Which reads can safely use replicas?
- How would you handle a hot short code?
- When would partitioning help, and what would you partition?
- Why is sharding not the first scaling step?
- How would you introduce `/api/v2` without breaking `/api/v1` clients?
- Which consistency guarantees are required immediately after URL creation?
- Which metrics would convince you that the architecture needs another scaling
  layer?
