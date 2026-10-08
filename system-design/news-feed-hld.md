# HLD — News Feed

## 1. Problem Statement

Design a news-feed service that lets users publish posts and read a personalized
home feed of recent posts from accounts they follow.

The design should remain responsive under a read-heavy workload while supporting
large follower counts, cursor pagination, caching, and horizontal scaling.

## 2. Functional Requirements

- Create and delete posts.
- Follow and unfollow users.
- Fetch a personalized home feed.
- Paginate the feed with a stable cursor.
- Show recent posts first.
- Avoid returning deleted posts.
- Support cache-backed feed reads.
- Handle users who follow very large accounts.
- Keep feed results reasonably fresh.

Out of scope:

- Full-text search.
- Ranking by machine-learning relevance.
- Media processing and video delivery.

## 3. Non-Functional Requirements

- Low p95 feed-read latency.
- High read availability.
- Horizontal scalability.
- Bounded cache memory.
- Eventual consistency is acceptable for feed propagation.
- A post should become visible to followers within a defined freshness target.
- A slow or unavailable cache should not make durable feed data unavailable.

## 4. High-Level Architecture

```text
                         +------------------+
                         |   Web / Mobile   |
                         +--------+---------+
                                  |
                               HTTPS
                                  |
                       +----------v-----------+
                       | Feed API / Gateway   |
                       +----------+-----------+
                                  |
                    +-------------+-------------+
                    |                           |
             +------v------+             +------v------+
             | Feed Cache  |             | Feed Service |
             | Redis       |             | / Read Path  |
             +------+------+\             +------+------+
                    |        \                    |
                    |         \                   |
                    |          +------------------+
                    |                             |
             +------v-----------------------------v------+
             |              Feed Storage                 |
             | PostgreSQL / sharded relational storage  |
             +-------------------+-----------------------+
                                 |
                          +------v------+
                          | Follow/Post |
                          | data model  |
                          +-------------+

Post creation
      |
      v
+-------------+       +------------------+
| Post Service| ----> | Queue / Workers  |
+------+------+       +--------+---------+
       |                        |
       |                        v
       |                Feed materialization
       |                for selected users
       v
  Post Storage
```

A production implementation can use a dedicated cache cluster and a durable
event stream. The exact technologies are less important than keeping the read
path bounded and the feed propagation work asynchronous.

## 5. Feed Generation Strategies

### Fan-out-on-read

At read time, fetch recent posts from all followed accounts and merge them.

Advantages:

- Simple writes.
- No per-follower feed materialization.
- Changes to follow relationships are immediately reflected by the read query.

Costs:

- Expensive for users following many accounts.
- Repeated reads repeat the same merge work.
- Hot users can create large query fan-out.

### Fan-out-on-write

When a user publishes, push a feed item into each follower's feed.

Advantages:

- Very fast reads.
- Feed ordering can be precomputed.
- Cache population is straightforward.

Costs:

- A post from a celebrity/high-fan-out account can create a huge write burst.
- Unused feed items consume storage.
- Follow/unfollow changes require careful reconciliation.

### Hybrid strategy

Use fan-out-on-write for ordinary accounts and fan-out-on-read for extremely
high-fan-out authors.

This keeps the common read path fast without forcing one post to synchronously
fan out to millions of followers.

## 6. Read Path

1. Authenticate the viewer.
2. Validate the requested page size and cursor.
3. Build a cache key from viewer, cursor, and page size.
4. Return the cached page on a hit.
5. On a miss, query the materialized feed or execute the bounded read query.
6. Cache the resulting page with a short TTL.
7. Return the page and the next cursor.
8. Record latency, cache hit/miss, and storage-query metrics.

The cache is an optimization, not the source of truth.

## 7. Cursor Pagination

Avoid deep `OFFSET` pagination because the database may need to scan and discard
increasing numbers of rows.

Prefer a stable ordering key such as `(created_at, post_id)` or a monotonic
`feed_item_id`.

Example:

```text
WHERE feed_item_id < :cursor
ORDER BY feed_item_id DESC
LIMIT 50
```

The cursor should be opaque at the API boundary if exposing internal identifiers
would leak implementation details.

## 8. Caching

Useful cache layers include:

- First-page home-feed cache.
- Short-lived subsequent-page cache.
- Post-object cache.
- User/following metadata cache.

Important controls:

- TTL with explicit freshness expectations.
- Versioned cache keys when response shape changes.
- Bounded page sizes.
- Stampede protection for hot keys.
- Negative caching only where absence is meaningful and safe.
- Invalidation after a post is deleted or a follow relationship changes.

Do not cache an unbounded complete feed for every user.

## 9. Data Model

Core relational entities:

- `users`
- `follows`
- `posts`
- `user_feed_items` for materialized feed entries when the hybrid/write path is used

Useful indexes:

- `(follower_id, followee_id)` for following lookups.
- `(author_id, created_at DESC, post_id DESC)` for author timelines.
- `(viewer_id, feed_item_id DESC)` for materialized feed reads.

## 10. Scaling

Monitor:

- Feed requests per second.
- p50/p95/p99 feed latency.
- Cache hit ratio.
- Database query latency and rows examined.
- Average following count.
- Follower distribution and high-fan-out authors.
- Feed materialization queue depth.
- Storage growth.
- Cache memory and eviction rate.

Scale in stages:

1. Index and measure the read query.
2. Add cursor pagination.
3. Add bounded caching.
4. Move expensive propagation to asynchronous workers.
5. Introduce a hybrid fan-out strategy.
6. Partition or shard only when measured data volume requires it.

## 11. Consistency and Freshness

Feed systems commonly accept eventual consistency.

Examples:

- A newly published post may take a short period to reach all followers.
- A follow action may not immediately populate every historical feed item.
- A deleted post should be filtered from reads even if an old materialized entry exists.

The system should define a freshness SLO rather than promising instantaneous global
propagation.

## 12. Failure Handling

### Cache failure

Fall back to the durable feed query or materialized store. Protect the database
with request limits and stampede controls.

### Worker backlog

Expose queue depth and age metrics. Apply bounded retries and prioritize fresh
feed propagation over unnecessary historical rebuilds.

### Database overload

Use read replicas where consistency permits, reduce page size, cache hot pages,
and shed non-critical requests before adding infrastructure blindly.

### Duplicate feed item

Use deterministic identifiers or uniqueness constraints so retried propagation
does not create duplicate visible entries.

## 13. Security

- Authenticate feed requests.
- Authorize follow/unfollow and post mutations.
- Enforce privacy rules before returning a post.
- Avoid putting sensitive user data into cache keys or values.
- Apply per-user and per-IP request limits.
- Treat cache contents as untrusted from an authorization perspective and re-check
  access where required.

## 14. Observability

Track:

- Request latency by endpoint and page depth.
- Cache hit/miss ratio.
- Feed query duration.
- Rows scanned versus returned.
- Materialization queue lag.
- Worker failures and retries.
- Duplicate propagation attempts.
- Freshness delay from post creation to feed visibility.

Correlate API requests, cache operations, database queries, and worker jobs with
a request or event identifier.

## 15. Key Trade-offs

| Decision | Option A | Option B | Recommended starting point |
| --- | --- | --- | --- |
| Feed generation | Fan-out-on-read | Fan-out-on-write | Hybrid |
| Pagination | OFFSET | Cursor | Cursor |
| Cache | Full feed | Bounded pages | Bounded pages |
| Propagation | Synchronous | Async workers | Async workers |
| Consistency | Strong | Eventual | Eventual for feed propagation |
| Scaling | Vertical | Horizontal | Horizontal after measurement |

The core interview point is that a News Feed is a read-heavy system where the
main design problem is controlling fan-out cost. Cursor pagination, bounded
caching, asynchronous propagation, and a hybrid fan-out strategy work together
to keep both read and write paths predictable.
