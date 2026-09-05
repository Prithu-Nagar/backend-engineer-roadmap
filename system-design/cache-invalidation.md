# Cache Invalidation, TTL & Cache Stampede

Day 36 focuses on Redis-backed caching patterns and the consistency problems
created when cached data can outlive or diverge from the source of truth.

---

## Cache-Aside

Cache-aside is a common application pattern.

```text
Request
   |
   v
Application
   |
   v
Cache ---- hit ----> Return cached value
   |
  miss
   |
   v
Database
   |
   v
Application
   |
   v
Cache.set(...)
   |
   v
Return value
```

The application owns the cache lookup and decides when to populate or
invalidate entries.

### Typical Flow

1. Build a stable cache key.
2. Read the cache.
3. Return the cached value on a hit.
4. Query the source of truth on a miss.
5. Store the result with an appropriate TTL.
6. Return the result to the caller.

---

## Cache Invalidation

When source data changes, an old cache entry may become stale.

A common write flow is:

```text
Write request
    |
    v
Database
    |
    v
Invalidate cache key
```

The ordering must be chosen deliberately. For a cache-aside service, updating
the source of truth and then invalidating the affected key is a simple baseline.
More complex systems may use versioning, events, or write-through patterns.

### Invalidation Strategies

- Explicit key deletion
- TTL expiration
- Versioned cache keys
- Event-driven invalidation
- Namespace or pattern-based invalidation where supported

No invalidation strategy is universally correct. The right choice depends on
freshness requirements, write frequency, and failure handling.

---

## TTL

A TTL limits how long an entry can remain available in the cache.

```text
set key -> value + TTL
                 |
                 v
            expiration
                 |
                 v
             cache miss
```

TTL helps bound staleness and provides automatic cleanup, but it does not
guarantee that data is fresh until the TTL expires.

Consider:

- How stale can the data safely become?
- How expensive is the underlying database query?
- How frequently does the source data change?
- What happens when many keys expire together?

---

## Cache Stampede

A cache stampede occurs when many requests miss the same hot key around the
same time and all query the underlying database.

```text
                 +--> Request 1 --> DB
Hot key expires -+--> Request 2 --> DB
                 +--> Request 3 --> DB
                 +--> Request 4 --> DB
```

This can overload the database precisely when the cache is least effective.

### Mitigation Techniques

- Request coalescing
- Per-key locks
- Short randomized TTL jitter
- Proactive refresh
- Stale-while-revalidate
- Warming critical keys

The mitigation should match the workload. A lock can reduce duplicate work, but
the lock itself must have a bounded lifetime and failure strategy.

---

## Redis Key Design

Good cache keys should be:

- Stable
- Namespaced
- Easy to invalidate
- Consistent across application instances

Example:

```text
expense:1001
expense:category:travel:2026-09
```

A shared Redis cache allows multiple application instances to observe the same
cached values, unlike a purely in-process cache.

---

## Failure Handling

The cache should normally be treated as an optimization rather than the only
copy of important data.

If Redis is unavailable:

1. Detect the cache failure.
2. Decide whether to bypass the cache.
3. Read from the source of truth when safe.
4. Monitor the failure and recovery.
5. Avoid turning a cache outage into a database overload.

A fallback strategy should include capacity planning because bypassing a cache
can sharply increase database traffic.

---

## Interview Questions

1. What is the cache-aside pattern?
2. When should a cache entry be invalidated?
3. What does TTL protect against, and what does it not guarantee?
4. What is a cache stampede?
5. How can request coalescing reduce a stampede?
6. How would you design Redis keys for per-resource caching?
7. What should an application do if Redis becomes unavailable?
8. How would you balance cache freshness against database load?
