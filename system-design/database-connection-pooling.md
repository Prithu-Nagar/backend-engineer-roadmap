# Database Connection Pooling

Day 31 introduces database connection pooling as a backend and distributed
systems capacity-management concern.

## What Is Connection Pooling?

A connection pool keeps a bounded set of database connections available for
reuse.

```text
Request A ──┐
Request B ──┼──> Connection Pool ──> Database
Request C ──┘
```

A request borrows a connection for a short unit of database work and returns it
to the pool when the work is complete.

## Why Use a Pool?

Creating a database connection can involve:

- Network setup
- Authentication
- TLS negotiation
- Session initialization
- Database-side resource allocation

Reusing established connections avoids repeating this setup for every request.

## Pool Saturation

A pool is intentionally bounded.

```text
Application
    |
    v
+-------------------+
| Connection Pool   |
| 1 | 2 | 3 | 4     |
+-------------------+
    |
    v
 Database
```

If all connections are busy, additional requests must wait, fail fast, or
time out according to the pool configuration.

Pool saturation can therefore become a throughput and latency bottleneck.

## Capacity Considerations

A useful first-order relationship is:

```text
Concurrent DB work <= Available pool connections
```

Increasing the pool size does not automatically increase throughput. The
database itself has limits on CPU, memory, I/O, locks, and concurrent work.

A practical design should consider:

1. Application instance count.
2. Pool size per instance.
3. Database connection limit.
4. Expected concurrent requests.
5. Query duration.
6. Transaction duration.
7. Timeout behavior.

For example, if an application runs 5 instances with a maximum pool size of
10 per instance, the application layer could potentially request up to:

```text
5 × 10 = 50 connections
```

The database must be able to support that total alongside administrative and
other service connections.

## Pool Lifecycle

```text
Request
   |
   v
Acquire connection
   |
   v
Execute short DB operation
   |
   v
Commit / rollback
   |
   v
Return connection
```

Connections should be returned even when the operation raises an exception.

## Common Failure Modes

### Pool Exhaustion

All connections are busy and requests queue behind the pool.

### Long Transactions

A transaction holds a connection longer than necessary and reduces pool
availability.

### Connection Leaks

A connection is not returned after an error, gradually exhausting the pool.

### Oversized Pool

Too many application connections overwhelm the database rather than improving
performance.

## Backend Guidelines

- Keep transactions short.
- Always release connections in a `finally`-equivalent lifecycle.
- Configure acquisition and idle timeouts.
- Monitor active, idle, and waiting connections.
- Size pools together with the number of application instances.
- Investigate slow queries before simply increasing pool size.

## Interview Questions

1. Why is connection pooling faster than creating a connection per request?
2. What happens when a pool is exhausted?
3. How does pool size interact with horizontal scaling?
4. Why can increasing pool size make database performance worse?
5. How do long-running transactions affect a connection pool?
6. What metrics would you monitor for pool health?
