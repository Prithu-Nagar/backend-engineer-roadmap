# Redis

Redis is an in-memory data store commonly used for caching, temporary data, counters, queues, and other low-latency workloads.

---

## Why Redis?

Redis stores frequently accessed data in memory, allowing applications to retrieve data faster than repeatedly querying a database.

A common architecture is:

Client
   ↓
Backend
   ↓
Redis
   ↓
Database

If the required data is already cached, the application can avoid a database query.

---

## Cache-Aside Pattern

The application checks Redis before querying the database.

Request
   ↓
Redis
   ↓
Cache Hit?
 ├── Yes → Return cached data
 └── No
       ↓
    Database
       ↓
    Store in Redis
       ↓
    Return data

The application remains responsible for deciding when data should be read from or written to the cache.

---

## Cache Keys

A consistent cache-key strategy makes cached data easier to identify and invalidate.

Examples:

task:123
user:123:tasks
user:123:task_count

Keys should be predictable and specific enough to avoid collisions.

---

## TTL

TTL (Time To Live) determines how long a cached value remains available.

Example:

task:123
TTL = 300 seconds

After the TTL expires, the cached value is removed and the application can retrieve fresh data from the database.

TTL is useful when cached data can become stale over time.

---

## Cache Invalidation

When database data changes, related cached data may need to be invalidated.

Example:

Update Task
     ↓
Update Database
     ↓
Delete task:123 from Redis

The next request can retrieve the updated data from the database and populate the cache again.

Cache invalidation is one of the main challenges when introducing caching into an application.

---

## Cache Hit

A cache hit occurs when the requested data is already present in Redis.

Request
   ↓
Redis
   ↓
Data Found
   ↓
Return Response

This avoids the database query.

---

## Cache Miss

A cache miss occurs when the requested data is not available in Redis.

Request
   ↓
Redis
   ↓
Data Not Found
   ↓
Database
   ↓
Store in Redis
   ↓
Return Response

---

## Redis vs Database

Redis should not automatically replace the primary database.

For an application such as the Task Manager:

PostgreSQL
    ↓
Source of Truth

Redis
    ↓
Cache

The database provides durable persistence while Redis provides fast access to frequently requested data.

---

## Common Redis Use Cases

Redis can be used for:

- Application caching
- Session storage
- Rate limiting
- Counters
- Temporary data
- Pub/Sub
- Queues
- Distributed locks

The appropriate use depends on the application's requirements.

---

## Advantages

- Very low latency
- Reduces database load
- Useful for frequently accessed data
- Supports expiration through TTL
- Supports multiple data structures
- Useful for distributed applications

---

## Trade-offs

- Additional infrastructure
- Cache invalidation complexity
- Possible stale data
- Additional memory usage
- Requires monitoring and operational management
- Application behavior becomes more complex

---

## Task Manager Application

For the Task Manager project, Redis can eventually be used to cache frequently requested task data.

A possible flow is:

GET /api/tasks/123
        ↓
      Redis
        ↓
   Cache Hit?
    /       \
  Yes        No
   ↓          ↓
Response    PostgreSQL
              ↓
         Store in Redis
              ↓
           Response

When a task is updated or deleted, the corresponding cache entry should be invalidated.

---

## Key Takeaway

Redis is most valuable when it solves a real performance or scalability problem.

A cache should complement the primary database rather than unnecessarily replace or complicate it.
