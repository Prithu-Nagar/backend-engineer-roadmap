# Day 79 — Full System Design Mock Interview

**Suggested duration:** 45–60 minutes  
**Prompt:** Design a news feed service for a social application.

## 1. Clarify requirements (5 minutes)

Ask about:
- Read and write volume, active users, geographic distribution, and growth.
- Feed ordering: reverse chronological, ranked, or a combination.
- Whether the feed is public, private, or follower-scoped.
- Freshness expectations and acceptable delay for new posts.
- Pagination, media support, deletion, blocking, and privacy requirements.

State assumptions before designing. Do not invent scale figures without labeling them as estimates.

## 2. Define APIs (5 minutes)

Example contracts:
- `POST /v1/posts` — create a post; require authentication and an idempotency strategy.
- `GET /v1/feed?cursor=...&limit=20` — retrieve a page of feed items.
- `DELETE /v1/posts/{post_id}` — delete or tombstone a post with ownership checks.

Specify validation, authorization, pagination behavior, error responses, and compatibility expectations.

## 3. High-level architecture (10 minutes)

Discuss:
- API gateway/load balancer and stateless application instances.
- Post service and durable post storage.
- Follow graph storage.
- Event/queue layer for fan-out and asynchronous processing.
- Feed generation workers and feed-item storage or cache.
- Object storage/CDN for media.
- Observability: metrics, structured logs, traces, and alerting.

Draw request and event flows, and identify the system of record for each entity.

## 4. Data model and feed strategy (10 minutes)

Core entities:
- `users(user_id, ...)`
- `follows(follower_id, followee_id, created_at)`
- `posts(post_id, author_id, created_at, body, visibility, status)`
- `feed_items(user_id, post_id, ranking_key, created_at)`

Compare **fan-out on write** for users with manageable follower counts against **fan-out on read** for high-follower accounts. Consider a hybrid strategy for celebrity accounts.

Explain indexes, cursor pagination, deduplication, deletion propagation, privacy checks, and feed rebuilds.

## 5. Reliability, consistency, and scale (10 minutes)

Address:
- Queue retries, dead-letter handling, idempotent consumers, and backpressure.
- Eventual consistency and the freshness SLO.
- Cache invalidation and stale feed items.
- Hot keys, high-follower accounts, and uneven partitions.
- Database replication, partitioning, and recovery.
- Rate limiting, abuse prevention, and authorization at read time.

Identify the top bottlenecks and the metrics that would reveal them.

## 6. Trade-offs and closing (5 minutes)

Summarize the simplest viable design, the first scaling bottleneck, and the next two improvements. Call out costs and failure modes rather than listing technologies without justification.

## Interviewer scorecard

| Area | Score (1–4) | Evidence / follow-up |
|---|---:|---|
| Requirements and assumptions |  |  |
| API and data model |  |  |
| Architecture and data flow |  |  |
| Scale estimates and bottlenecks |  |  |
| Reliability and security |  |  |
| Trade-offs and communication |  |  |

## Self-review

- Did I clarify requirements before proposing components?
- Did I explain why each storage or queue choice fits the workload?
- Did I cover pagination, privacy, retries, and failure recovery?
- Did I distinguish strong consistency needs from eventual consistency?
- Did I communicate trade-offs and revisit assumptions as scale changed?
