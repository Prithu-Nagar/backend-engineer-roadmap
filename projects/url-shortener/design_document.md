# URL Shortener — Design Document

## Day 65

This document turns the Day 64 HLD into a design artifact that can be used in
an interview or architecture review. It records requirements, API contracts,
data ownership, scaling choices, and the evolution path for the existing
URL Shortener project.

---

## 1. Requirements

### Functional Requirements

- Create a short URL for a valid HTTP(S) destination.
- Redirect a short code to its destination.
- Retrieve metadata for an owned short URL.
- Support active/inactive and expiration state.
- Enforce unique short codes.
- Support explicit API-versioned contracts.

### Non-Functional Requirements

- Low-latency redirects.
- Durable URL mappings.
- Horizontally scalable application instances.
- High availability for the read-heavy redirect path.
- Observable latency, errors, traffic, and saturation.
- Clear data ownership between services.

---

## 2. API Contract

### Create URL

```http
POST /api/v1/urls
Content-Type: application/json
Idempotency-Key: <client-operation-id>
```

Request:

```json
{
  "original_url": "https://example.com/backend"
}
```

Response:

```json
{
  "id": "url-123",
  "short_code": "aB91x",
  "short_url": "https://short.example/aB91x"
}
```

### Redirect

```http
GET /aB91x
```

The redirect handler looks up the short code, validates active/expiration
state, and returns the configured redirect response.

### Versioning

A future contract can be introduced without silently changing v1:

```http
POST /api/v2/urls
```

Version-specific serialization should live at the API boundary while the core
URL creation policy remains reusable.

---

## 3. Service Ownership

```text
                 +----------------+
                 |  API Gateway   |
                 +-------+--------+
                         |
              +----------+----------+
              |                     |
              v                     v
       +-------------+       +-------------+
       | URL Service |       | User Service |
       +------+------+       +------+------+
              |                     |
           URL DB                User DB
              |
            Cache
```

### URL Service Owns

- Short-code generation/validation.
- Destination URL.
- URL lifecycle state.
- Expiration.
- Redirect behavior.
- URL-specific metadata.

### User Service Owns

- Identity.
- Account lifecycle.
- Authentication-related user data.

The URL Service stores an external owner identifier rather than creating a
foreign key into the User Service database.

---

## 4. Data Model

Conceptual URL record:

| Field | Purpose |
|---|---|
| `short_url_id` | Stable internal identifier |
| `short_code` | Public lookup key; unique |
| `original_url` | Redirect destination |
| `owner_user_id` | External identity reference |
| `is_active` | Lifecycle state |
| `created_at` | Creation timestamp |
| `expires_at` | Optional expiration |

Important database constraints:

- Unique constraint on `short_code`.
- Valid lifecycle values.
- Index on `short_code` for redirect lookup.
- Owner/time index for metadata queries.

---

## 5. Redirect Flow

```text
Client
  |
  v
Gateway
  |
  v
URL Service
  |
  +--> cache lookup
  |      |
  |      +--> hit --> state check --> redirect
  |
  +--> database lookup
         |
         +--> state check
         |
         +--> cache population
         |
         v
      redirect
```

The User Service is not part of the redirect path because the URL Service
already owns the information needed to resolve the short code. This keeps the
latency-critical path smaller and prevents user-service availability from
becoming a redirect dependency.

---

## 6. Create Flow

```text
Client
  |
  v
Gateway
  |
  v
URL Service
  |
  +--> validate destination
  |
  +--> authenticate / authorize
  |
  +--> generate short code
  |
  +--> insert with unique constraint
  |
  +--> return URL
```

The database is the final concurrency boundary for uniqueness. If two requests
choose the same candidate code, one insert succeeds and the other is rejected
and retried with another candidate.

---

## 7. Scaling Plan

### Application

Run stateless URL Service instances behind a load balancer.

### Cache

Cache hot redirect mappings with a bounded TTL. Add invalidation when URL
state changes.

### Database

Start with a relational primary and well-designed indexes. Add read replicas
for reads that tolerate replica lag. Partition large append-heavy event tables
when measurable volume justifies it.

### Sharding

Do not introduce sharding solely because the system is described as
"high-scale." First measure database CPU, I/O, connection saturation, query
latency, and storage growth. If a single database becomes the measured limit,
select a shard key that matches the dominant access pattern and plan for
rebalancing and operational complexity.

---

## 8. Reliability

| Failure | Design response |
|---|---|
| Cache outage | Database fallback |
| Database read timeout | Controlled error and observability |
| Duplicate short code | Unique constraint + retry |
| App instance failure | Load balancer health checks |
| Replica lag | Route consistency-sensitive reads to primary |
| User service outage | Redirect remains independent |
| Duplicate create request | Idempotency key where supported |

---

## 9. Observability

Track:

- Redirect/create QPS.
- p50/p95/p99 latency.
- Cache hit ratio.
- Database query latency.
- Connection-pool utilization.
- Replica lag.
- Error/timeout rate.
- Short-code collision rate.
- Storage growth.

A request ID should connect gateway, application, cache, and database telemetry
for a single request.

---

## 10. API Evolution Strategy

The first version should have an explicit contract and documented deprecation
policy.

Migration sequence:

1. Freeze the v1 response contract.
2. Introduce v2 with the new representation.
3. Keep core domain/application logic shared.
4. Test v1 and v2 contracts independently.
5. Publish a migration/deprecation timeline.
6. Remove v1 only after the compatibility window and usage review.

This prevents an apparently small serializer change from becoming an accidental
breaking change for existing clients.

---

## 11. Interview Summary

The design can be explained in this order:

1. Establish the read-heavy redirect workload.
2. Define URL and User service ownership.
3. Show the database as the source of truth for mappings and uniqueness.
4. Add a cache to optimize hot reads.
5. Scale application instances horizontally.
6. Add replicas/partitioning only for measured workloads.
7. Define failure and consistency behavior.
8. Explain API versioning and backward compatibility.
9. Close with metrics that determine the next architectural change.
