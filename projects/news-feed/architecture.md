# News Feed — Architecture

## Day 69

Day 69 turns the News Feed HLD into a project-oriented architecture artifact
for implementation planning and interview discussion.

## Architecture

```text
Client
  |
  v
Feed API
  |
  +----> Redis / Feed Cache
  |
  +----> Feed Service ----> PostgreSQL / Feed Store
  |
  +----> Follow/Post data

Post creation
  |
  v
Post Service
  |
  v
Queue / Worker
  |
  +----> Materialized feed items
  +----> Cache invalidation
```

## Core Flows

### Read Feed

1. Authenticate the viewer.
2. Validate page size and cursor.
3. Check the bounded feed-page cache.
4. On a miss, query the materialized feed or execute the indexed read query.
5. Cache the result for a short TTL.
6. Return items and an opaque next cursor.
7. Record latency and cache-hit metrics.

### Publish Post

1. Authenticate the author.
2. Persist the post.
3. Publish a feed-propagation event.
4. Workers materialize the post for eligible followers where fan-out-on-write
   is appropriate.
5. Invalidate or version affected first-page cache entries.
6. Use retry-safe identifiers so repeated events do not create duplicates.

### Follow / Unfollow

1. Validate the target user.
2. Persist the relationship change.
3. Invalidate affected first-page caches.
4. Reconcile materialized feed state asynchronously when required.

## Fan-Out Policy

The project uses a hybrid policy:

- Normal accounts can use fan-out-on-write for fast reads.
- Very high-fan-out accounts are read on demand to avoid massive write bursts.
- The threshold should be data-driven and observable rather than hard-coded as a
  universal constant.

## Pagination

Use cursor pagination instead of deep offsets.

A cursor can represent the last `(created_at, post_id)` pair or a monotonic
materialized `feed_item_id`. The API should keep the cursor opaque.

## Caching

Cache only bounded pages rather than an entire feed.

Recommended controls:

- Short TTL.
- Versioned keys.
- First-page priority.
- Stampede protection for hot users.
- Explicit invalidation after mutations.
- Durable storage remains the source of truth.

## Reliability Checklist

- [ ] Feed reads use stable cursor pagination.
- [ ] Cache failure falls back to durable storage.
- [ ] Feed propagation is asynchronous.
- [ ] High-fan-out authors do not cause unbounded synchronous writes.
- [ ] Duplicate propagation is idempotent.
- [ ] Deleted/private posts are filtered before delivery.
- [ ] Queue lag and feed freshness are observable.
- [ ] Database queries are reviewed with realistic `EXPLAIN` plans.
- [ ] Cache keys do not expose sensitive data.
