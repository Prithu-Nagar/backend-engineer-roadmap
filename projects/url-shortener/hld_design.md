# URL Shortener — HLD

## Day 64

This artifact turns the existing URL Shortener requirements into a high-level
design with explicit traffic assumptions, service boundaries, data ownership,
scaling choices, and failure considerations.

The capacity figures are illustrative planning assumptions and should be
replaced with measured product requirements in a real system.

---

## Requirements

### Functional

- Create a short URL from a valid destination URL.
- Redirect a short code to the original destination.
- Retrieve metadata for an owned short URL.
- Support expiration and active/inactive state.
- Enforce unique short codes.

### Non-Functional

- Low-latency redirects.
- High availability for read-heavy traffic.
- Durable URL mappings.
- Horizontally scalable application instances.
- Explicit data ownership.
- Observable latency, errors, traffic, and saturation.

---

## Capacity Assumptions

| Metric | Assumption |
|---|---:|
| New URLs / month | 100 million |
| Redirects / month | 1 billion |
| Peak multiplier | 5x |
| Average mapping size | 1 KB |

Approximate average traffic:

```text
Creates:
100,000,000 / 30 days ≈ 38.6 requests/second

Redirects:
1,000,000,000 / 30 days ≈ 386 requests/second
```

Using a 5x peak multiplier:

```text
Create peak     ≈ 193 requests/second
Redirect peak   ≈ 1,930 requests/second
```

Approximate raw mapping storage:

```text
100,000,000 × 1 KB ≈ 100 GB/month
```

Indexes, replication, backups, and database overhead require additional
capacity.

---

## High-Level Architecture

```text
                         +----------------+
Client ---------------->| API Gateway    |
                         +-------+--------+
                                 |
                         +-------+-------+
                         |               |
                         v               v
                  +-------------+  +-------------+
                  | URL Service |  | User Service|
                  +------+------+  +------+------+
                         |                |
                         v                v
                      URL DB           User DB
                         |
                         v
                       Cache
```

The URL Service owns URL mappings. The User Service owns user identity data.
The services should not directly query each other's databases.

---

## Request Flows

### Create URL

```text
Client
  |
  v
API Gateway
  |
  v
URL Service
  |
  +--> Validate URL
  |
  +--> Generate/check short code
  |
  +--> Persist mapping
  |
  v
Response
```

The database remains authoritative for short-code uniqueness.

### Redirect

```text
Client
  |
  v
API Gateway
  |
  v
URL Service
  |
  +--> Cache lookup
  |       |
  |       +--> Hit --> Redirect
  |
  +--> URL DB lookup
          |
          +--> Populate cache
          |
          v
       Redirect
```

The redirect path is read-heavy, so caching is a natural optimization after
correctness and database indexing are established.

---

## Data Ownership

### URL Service

Owns:

- Short code
- Original URL
- Owner identifier
- Creation time
- Expiration
- Active state

### User Service

Owns:

- User identity
- Email
- Account lifecycle

The URL service may store the user identifier as an external reference, but
should not create a database-level foreign key into the User Service database.

---

## Scaling Strategy

### Application Layer

Keep URL Service instances stateless and place them behind a load balancer.

```text
                 Load Balancer
                 /     |                      v      v       v
             URL API URL API URL API
```

### Database

Start with:

- Relational primary database
- Unique index on short code
- Owner/time index for metadata queries
- Active/short-code lookup path

Scale later with:

- Read replicas for read-heavy workloads
- Partitioning for large historical datasets
- Archival for expired records

### Cache

Cache:

```text
short_code -> original_url
```

Define:

- TTL
- Invalidation behavior
- Negative caching policy
- Stampede protection
- Cache failure fallback

---

## Reliability and Failure Modes

| Failure | Expected behavior |
|---|---|
| Cache unavailable | Read from URL database |
| URL database read failure | Return a controlled service error |
| Duplicate short code | Reject and retry generation |
| Expired URL | Return the defined inactive/expired response |
| Application instance failure | Load balancer routes to another instance |
| User service unavailable during redirect | Redirect should not require a user-service lookup |
| Repeated create retry | Use an idempotency strategy where the API contract supports it |

---

## Trade-offs

### Relational Database

Provides strong uniqueness and durable mapping storage with familiar indexing
and transaction semantics.

### Cache

Reduces repeated database reads on the redirect path but introduces TTL,
invalidation, and consistency considerations.

### Database-per-Service

Improves ownership and service autonomy but makes cross-service queries and
transactions more complex.

### Premature Sharding

Sharding can increase operational complexity. It should follow evidence from
data size, throughput, and access-pattern limits rather than being the first
scaling step.

---

## Interview Discussion Points

- Why is redirect traffic modeled separately from URL creation?
- Which component is the source of truth for short-code uniqueness?
- Why can the redirect path avoid the User Service?
- What happens if the cache is unavailable?
- When would read replicas become useful?
- What metrics would justify partitioning or sharding?
- How would custom aliases affect the uniqueness model?
- How would analytics change the write/read architecture?
