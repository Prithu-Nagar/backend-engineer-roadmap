# URL Shortener — Mock System Design Interview

Use this artifact for a 35–45 minute mock interview. State assumptions before
estimating capacity, and explain the reason for each major design choice.

## 1. Clarify Requirements (5 minutes)

Functional requirements:

- Create a short code for a valid long URL.
- Redirect a short URL to its destination.
- Support optional expiration and custom aliases if required.
- Let authenticated owners inspect or deactivate links if account management is
  in scope.

Non-functional requirements:

- Redirects should have low latency and high availability.
- Codes must be unique and redirects must not silently change destinations.
- The system should tolerate traffic spikes and protect against abuse.
- Define retention, privacy, analytics freshness, and availability expectations.

Ask whether links are editable, whether custom aliases are required, and whether
analytics must be real time. These choices affect schema, cache invalidation,
and write/read paths.

## 2. Estimate Capacity (5 minutes)

Choose explicit illustrative assumptions rather than presenting estimates as
facts. For example, if the service receives 100 million redirects per day:

- Average redirect rate is approximately 100,000,000 / 86,400, or 1,157 requests
  per second.
- A peak multiplier of 5 implies roughly 5,800 redirects per second at peak.
- If creation volume is 1 million links per day, it is about 12 creates per
  second on average before peak factors.
- Estimate storage from rows, indexes, metadata, retention, and replication.

Discuss how a higher read/write ratio favors cache capacity and how long-lived
links affect durable storage and key-management decisions.

## 3. APIs and Data Model (5 minutes)

Example API contracts:

- `POST /api/v1/urls` — validate a destination and create a short code.
- `GET /{code}` — resolve the code and return an HTTP redirect.
- `GET /api/v1/urls/{code}` — retrieve owner-authorized metadata if required.
- `DELETE /api/v1/urls/{code}` — deactivate a link if lifecycle controls are in
  scope.

A URL record may include `code`, `original_url`, `owner_id`, `created_at`,
`expires_at`, `is_active`, and optional metadata. Add a unique constraint on
`code`. Decide whether aliases are case-sensitive and how deleted or expired
codes behave. Never assume a short code is authorization to view private data.

## 4. High-Level Architecture (8 minutes)

A practical baseline:

1. Client reaches a load balancer or edge layer.
2. Redirect requests reach stateless redirect services.
3. The service checks a distributed cache, then reads the durable database on
   a cache miss.
4. Valid mappings are cached with a TTL; create/deactivate operations update
   durable state and coordinate cache invalidation.
5. Link creation uses a write service that validates URLs and allocates a unique
   code, then persists the mapping.
6. Click analytics, if required, are published asynchronously so a slow
   analytics sink does not block the redirect path.

Start with a relational database and a cache only when justified. Add sharding,
read replicas, or regional routing when observed scale or availability targets
require them.

## 5. Code Generation and Data Integrity (5 minutes)

Possible strategies include random base62 codes with collision checks, a
sequence encoded as base62, or a carefully designed distributed ID scheme.
Random codes need a unique constraint and bounded retry on collision. Sequential
codes can reveal creation volume and may be guessable. Explain entropy, collision
probability, hot partitions, and alias conflicts for the chosen strategy.

The database remains the source of truth. Define how creation retries behave,
including whether an idempotency key is needed to avoid duplicate records after
client timeouts.

## 6. Caching and Failure Handling (5 minutes)

- Cache key: normalized short code; value: destination and relevant state.
- Use a TTL and explicit invalidation for deactivation or destination changes.
- Protect the database from cache stampedes with request coalescing or bounded
  refresh strategies when justified.
- Decide how cache outages degrade: bypass cache with strict database limits,
  serve only safe stale entries, or fail according to the product's correctness
  requirements.
- Apply timeouts, bounded retries, circuit breaking, and observability to
  dependencies.

A cached redirect must not bypass expiration, deactivation, or security policy
beyond the accepted staleness window.

## 7. Abuse, Security, and Operations (5 minutes)

- Validate URL schemes and reject dangerous or unsupported destinations.
- Rate-limit link creation and protect against automated abuse.
- Consider phishing/malware reporting, domain reputation, takedown workflows,
  and safe preview behavior.
- Avoid turning the redirect service into an SSRF-capable URL fetcher.
- Record metrics for redirect latency, cache hit rate, database errors, create
  failures, code collisions, expired links, and abuse reports.
- Use privacy-aware analytics, access controls, retention limits, and audit logs
  for administrative actions.

## Follow-up Questions

1. How would you support custom aliases without race conditions?
2. What happens if the cache and database disagree after a link is deactivated?
3. How would you migrate to sharded storage without changing the public API?
4. How would you preserve redirect availability during a database outage?
5. How would you prevent hot keys from overwhelming one cache node?
6. Which metrics and alerts would detect a redirect latency regression?
7. What changes if the product requires regional disaster recovery?

## Interview Evaluation Checklist

- [ ] Clarified requirements and explicitly stated assumptions.
- [ ] Estimated average and peak load with understandable arithmetic.
- [ ] Defined API contracts and a data model with uniqueness guarantees.
- [ ] Traced create and redirect requests end to end.
- [ ] Explained code generation, cache invalidation, and failure behavior.
- [ ] Covered abuse prevention, observability, and privacy.
- [ ] Compared alternatives and identified the next likely bottleneck.
