# Caching

Caching stores frequently accessed data in a faster storage layer to reduce latency and database load.

---

## Basic Flow

Client
  ↓
Application
  ↓
Cache
  ↓
Database

### Cache Hit

Data is found in the cache and can be returned immediately.

Request → Cache → Data Found → Response

### Cache Miss

Data is not found in the cache, so the application retrieves it from the database.

Request
  ↓
Cache Miss
  ↓
Database
  ↓
Store in Cache
  ↓
Response

---

## Cache-Aside

The application manages the cache explicitly.

data = cache.get(key)

if data is not None:
    return data

data = database.get(key)
cache.set(key, data)

return data

This is a common caching pattern for backend applications.

---

## TTL

**Time To Live (TTL)** defines how long cached data remains valid.

Cache Entry
    ↓
TTL = 300 seconds
    ↓
Entry expires

TTL helps prevent stale data from remaining indefinitely.

---

## Cache Invalidation

When underlying data changes, the corresponding cached data may become stale.

Database Update
      ↓
Invalidate Cache

Cache invalidation is one of the main challenges when designing cached systems.

---

## Cache Eviction

When cache storage becomes full, entries may need to be removed.

Common strategies:

| Strategy | Description                           |
| -------- | ------------------------------------- |
| LRU      | Removes least recently used entries   |
| LFU      | Removes least frequently used entries |
| FIFO     | Removes oldest entries first          |

---

## Write Strategies

### Write-Through

Data is written to the cache and database during the write operation.

Application
    ↓
Cache
    ↓
Database

### Write-Back

Data is initially written to the cache and persisted to the database later.

This can improve write performance but introduces consistency considerations.

### Read-Through

The cache retrieves missing data from the underlying data store.

---

## Cache Problems

### Cache Stampede

A popular entry expires and many requests simultaneously hit the database.

Cache Expiry
     ↓
Many Requests
     ↓
Database
     ↓
High Load

Possible mitigations:

- Request coalescing
- Locking
- Early refresh
- Randomized TTLs

### Cache Penetration

Repeated requests are made for data that does not exist.

Possible mitigations:

- Cache negative results
- Input validation
- Bloom filters

### Cache Avalanche

Many cached entries expire around the same time.

Possible mitigations:

- Randomized TTLs
- Staggered expiration
- Cache warming
- Rate limiting

---

## Redis

Redis is commonly used as an in-memory data store and caching layer.

A typical backend architecture:

Client
  ↓
Flask Application
  ↓
Redis
  ↓
PostgreSQL

Redis handles frequently accessed data while PostgreSQL remains the persistent source of truth.

---

## Caching in the Task Manager API

Caching could be introduced for frequently requested task data.

Example:

GET /tasks
     ↓
Check Cache
     ↓
 ┌───────────┐
 │           │
Hit         Miss
 │           │
 ↓           ↓
Return    Database
            ↓
        Update Cache
            ↓
         Return

Example cache key:

tasks:all

When tasks are created, updated, or deleted, the relevant cache entry should be invalidated or updated.

---

## Cache vs Database

| Feature     | Cache                    | Database           |
| ----------- | ------------------------ | ------------------ |
| Purpose     | Fast access              | Persistent storage |
| Speed       | Very fast                | Generally slower   |
| Persistence | Usually temporary        | Persistent         |
| Typical use | Frequently accessed data | Source of truth    |
| Size        | Usually smaller          | Usually larger     |

A cache should generally not replace the primary persistent database.

---

## Benefits

- Lower latency
- Reduced database load
- Higher throughput
- Better scalability

## Trade-offs

- Additional infrastructure
- Cache invalidation complexity
- Potential stale data
- Additional memory usage
- More complicated debugging

---

## Key Takeaways

Cache Hit
Cache Miss
TTL
Cache Invalidation
LRU
LFU
Cache-Aside
Read-Through
Write-Through
Write-Back
Cache Stampede
Cache Penetration
Cache Avalanche
Redis

**Core idea:** Caching improves application performance by serving frequently accessed data from a faster layer while carefully managing freshness and consistency.

