# HLD — Requirements and Capacity Estimates

## Day 64

## Goal

Turn a system-design prompt into explicit functional requirements,
non-functional requirements, traffic assumptions, storage estimates, and
initial architectural constraints before selecting components.

The numbers below are illustrative assumptions for a URL Shortener exercise.
They are not production measurements.

---

## Functional Requirements

### Core

- Create a short URL for a valid destination.
- Redirect a short code to its destination.
- Retrieve metadata for an owned short URL.
- Support expiration and active/inactive state.
- Prevent duplicate short-code ownership.

### Optional Later Features

- Custom aliases
- Link analytics
- Abuse detection
- Per-user quotas
- Administrative deactivation

Optional features should not be allowed to silently change the initial capacity
model.

---

## Non-Functional Requirements

- Low redirect latency.
- High availability for redirect traffic.
- Durable storage for URL mappings.
- Horizontal scaling for stateless API instances.
- Clear service/data ownership.
- Safe retries and idempotent create operations where applicable.
- Observability for request rate, latency, errors, and saturation.

---

## Capacity Assumptions

Use explicit assumptions before calculating capacity.

Example starting assumptions:

| Metric | Illustrative assumption |
|---|---:|
| New URLs / month | 100 million |
| Redirects / month | 1 billion |
| Average redirect-to-create ratio | 10:1 |
| Average stored mapping size | 1 KB |
| Peak traffic multiplier | 5x average |
| Working days for rough estimate | 30 |

These values are intentionally adjustable. A real design should replace them with
product or production data.

---

## Request Rate

Approximate average create rate:

```text
100,000,000 / (30 × 24 × 60 × 60)
≈ 38.6 creates/second
```

Approximate average redirect rate:

```text
1,000,000,000 / (30 × 24 × 60 × 60)
≈ 386.0 redirects/second
```

With a 5x peak multiplier:

```text
Peak creates     ≈ 193 requests/second
Peak redirects   ≈ 1,930 requests/second
```

These are planning values, not guarantees.

---

## Storage Estimate

At an illustrative 1 KB per stored mapping:

```text
100,000,000 × 1 KB
≈ 100 GB/month
```

Over 12 months:

```text
100 GB × 12
≈ 1.2 TB
```

The real footprint will be larger after indexes, database page overhead,
replication, backups, and metadata are included.

---

## Initial Architecture

```text
                    +----------------+
Client ------------> API Gateway    |
                    +-------+--------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
          URL Service             Identity Service
                 |                     |
                 v                     v
              URL DB               User DB
                 |
                 v
               Cache
```

Redirect traffic is a read-heavy path, so a cache can reduce repeated database
lookups. Cache correctness and invalidation rules must remain explicit.

---

## Scaling Constraints

### Stateless Application Layer

URL and identity service instances should remain horizontally scalable.

```text
                 Load Balancer
                 /     |                      v      v       v
             URL API URL API URL API
```

Session state should not be required inside an individual application instance.

### Database

Start with a primary relational database and indexes aligned with:

- Short-code lookup
- Owner + creation time
- Active/expiration filtering

Introduce read replicas or partitioning only when measured workload and data
growth justify the additional complexity.

### Cache

A cache can store:

```text
short_code -> destination
```

A suitable cache policy should define:

- TTL
- Invalidation on deactivation/update
- Negative caching, if used
- Stampede protection
- Maximum object size

---

## Reliability Considerations

- Database failures should not corrupt URL ownership state.
- Cache failures should degrade to database reads rather than break redirects.
- Create requests should use idempotency where clients may safely retry.
- Short-code uniqueness must be enforced by the authoritative datastore.
- Expired links should have deterministic redirect behavior.
- External dependencies should have timeouts and bounded retries.

---

## Interview Checklist

- What are the functional and non-functional requirements?
- Which assumptions drive the capacity estimate?
- How do average and peak QPS differ?
- Which data is read-heavy?
- Where would caching help?
- What is the authoritative source of truth?
- What happens when the cache is unavailable?
- When would replicas or partitioning become necessary?
- Which numbers should be measured rather than assumed?
