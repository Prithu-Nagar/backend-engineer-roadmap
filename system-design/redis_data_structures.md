# Day 16 — Redis Data Structures & Caching Patterns

## Redis

Redis is an in-memory data store commonly used for:

- caching
- sessions
- counters
- rate limiting
- queues
- temporary state

---

## Redis Data Structures

### String

Simple key-value data.

```text
user:1:name -> "Alex"

Useful for:

cached values
counters
flags
tokens
Hash

Useful for object-like data.

user:1
    name -> Alex
    role -> developer
    active -> true

Useful when multiple related fields belong to one entity.

List

Ordered collection.

Potential uses:

queues
recent activity
ordered events
Set

Collection of unique values.

Example:

online_users

Useful for:

unique membership
tags
relationship sets
Sorted Set

Unique members with scores.

Useful for:

leaderboards
rankings
priority-based data
Cache-Aside Pattern

The application checks Redis first.

Request
   |
   v
Redis
   |
   +---- HIT ----> Return
   |
   +---- MISS
          |
          v
       Database
          |
          v
       Redis
          |
          v
       Return
Cache Hit

If the requested value exists:

Application
     |
     v
   Redis
     |
    HIT
     |
     v
 Response

The database does not need to be queried.

Cache Miss

If the value isn't present:

Application
     |
     v
   Redis
     |
    MISS
     |
     v
 Database
     |
     v
 Redis SET
     |
     v
 Response
TTL

TTL means Time To Live.

A cache entry can have an expiration time.

task:123
TTL = 300 seconds

After expiration, the entry is no longer considered valid.

Cache Invalidation

When database data changes, cached data may become stale.

Possible approaches include:

Delete on write
UPDATE database
       |
       v
DELETE cache
Update cache on write
UPDATE database
       |
       v
UPDATE cache
TTL-based expiration

Allow the cache to expire automatically.

Important Trade-off

Caching improves:

latency
database load
scalability

But introduces:

stale data
invalidation complexity
additional infrastructure
cache consistency concerns
Day 16 Mental Model
Client
  |
  v
API
  |
  v
Service
  |
  +------> Redis
  |
  +------> Database

Redis is a performance layer.

The persistent database remains the source of truth.