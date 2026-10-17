# News Feed — Mock System Design Interview

## Interview Goal

Design a personalized home feed for users who publish posts and follow other
users. Target a read-heavy workload, stable pagination, low tail latency, and
eventual consistency for feed propagation.

**Suggested time:** 35–45 minutes.

## 1. Clarify Requirements (5 minutes)

Functional:
- Publish and delete posts.
- Follow and unfollow accounts.
- Read a personalized feed ordered by recency.
- Support cursor pagination and hide deleted or private posts.
- Refresh the feed as new posts arrive.

Non-functional:
- High read availability and low p95 latency.
- Horizontal scaling and bounded resource usage.
- Eventual consistency for feed propagation is acceptable.
- Cache failures must not make durable data unavailable.

Ask about expected DAU, reads/writes per user, follower distribution, freshness
target, retention, privacy rules, and ranking requirements before estimating.

## 2. APIs and Data Model (5 minutes)

Example endpoints:
- `POST /v1/posts`
- `DELETE /v1/posts/{post_id}`
- `PUT /v1/users/{user_id}/following/{target_id}`
- `DELETE /v1/users/{user_id}/following/{target_id}`
- `GET /v1/feed?cursor=...&limit=50`

Core records:
- `users(user_id, ...)`
- `posts(post_id, author_id, body, created_at, deleted_at, visibility)`
- `follows(follower_id, followee_id, created_at)`
- `feed_items(user_id, post_id, created_at)`

Use uniqueness constraints for follow relationships and feed-item identity.
Choose indexes based on actual access paths, for example follows by follower and
posts by author plus descending creation time.

## 3. High-Level Architecture (8 minutes)

```text
Clients
   |
API Gateway / Authentication
   |
Feed API -------- Redis (bounded page cache)
   |
Feed Service ---- Feed Store / PostgreSQL
   |
Post Service ---- Posts Store
   |
Outbox / Event Stream
   |
Workers --------- Feed Materialization
```

Keep durable post/follow state separate from cache. Publish feed events through
a transactional outbox or another reliable event-publication design so a
committed post is not silently lost between database commit and event publish.

## 4. Feed Generation Trade-Offs (7 minutes)

**Fan-out-on-read:** fetch recent posts from followed accounts and merge at
read time. It simplifies writes but can become expensive for users following
many accounts.

**Fan-out-on-write:** materialize feed items for followers when a post arrives.
It makes reads fast but creates write amplification for high-fan-out authors.

**Hybrid:** materialize ordinary accounts and read high-fan-out authors on
demand. Set the threshold from measured workload, not a universal constant.

Discuss feed freshness, follow/unfollow reconciliation, deleted posts, duplicate
events, and the impact of celebrity accounts.

## 5. Pagination, Caching, and Consistency (5 minutes)

- Use an opaque cursor based on a stable ordering key such as
  `(created_at, post_id)`; avoid deep `OFFSET` pagination.
- Cache bounded pages, especially the first page, with a short TTL.
- Include viewer identity and cursor/page size in cache keys.
- Prevent cache stampedes and fall back to durable storage on cache failure.
- Use idempotent feed-item writes and reconcile asynchronous propagation.
- Filter deleted/private posts before returning them.

## 6. Reliability and Observability (5 minutes)

Discuss queue lag, retry budgets, dead-letter handling, idempotent consumers,
database slow queries, cache hit rate, p95/p99 latency, feed freshness, and
partial dependency failure. Explain how to prevent retries from amplifying an
outage.

## 7. Capacity and Bottlenecks

Estimate storage and throughput only after stating assumptions:
- Daily active users and feed reads per user.
- Average posts per author and follower distribution.
- Feed-item write amplification under fan-out-on-write.
- Cache memory for active users' bounded pages.
- Queue throughput and acceptable propagation delay.

Identify the likely first bottleneck and explain what metric would confirm it.

## 8. Interview Scorecard

- [ ] Requirements and assumptions were explicit.
- [ ] APIs and data model support privacy and stable ordering.
- [ ] Fan-out strategy includes high-fan-out accounts.
- [ ] Pagination and cache behavior are bounded.
- [ ] Event delivery is retry-safe and observable.
- [ ] Failure modes and consistency trade-offs were explained.
- [ ] Estimates and proposed indexes follow stated access patterns.

## Follow-Up Questions

1. How would you delete a post already materialized in millions of feeds?
2. What happens if a feed worker processes the same event twice?
3. How would you support ranking without breaking cursor stability?
4. How do you prevent one high-fan-out account from starving ordinary events?
5. Which consistency guarantees are essential, and which can be eventual?
