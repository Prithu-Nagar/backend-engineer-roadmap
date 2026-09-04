# Read Replicas & Replication Lag

Day 35 focuses on scaling read-heavy database workloads with read replicas and
on the consistency trade-offs introduced by asynchronous replication.

## Primary and Replicas

A primary database accepts writes. One or more replicas receive replicated
changes and serve eligible read traffic.

```text
                 +----------------+
Writes --------> |    Primary     |
                 +-------+--------+
                         |
                    Replication
                    /          \
                   v            v
          +---------------+  +---------------+
          |   Replica 1   |  |   Replica 2   |
          +---------------+  +---------------+
                 ^                 ^
                 |                 |
              Read traffic for eventually consistent queries
```

## Why Use Read Replicas?

Read replicas can help when:

- Read traffic is much larger than write traffic.
- Queries are expensive enough to compete with writes on the primary.
- Additional read capacity is needed without immediately sharding the dataset.
- Reporting or analytical reads can tolerate some replication delay.

Replication does not automatically increase write capacity. Writes still need
to reach the primary unless a different multi-primary architecture is used.

## Replication Lag

With asynchronous replication, a committed write on the primary may not yet be
visible on a replica.

```text
Primary:  write A ----> commit
                         |
                         | replication delay
                         v
Replica:  replay A ----> visible
```

Lag can result from network delay, replica CPU or I/O pressure, long-running
queries, or a replication backlog.

## Read Routing

The application should choose the read destination based on consistency needs.

| Request | Preferred destination |
| --- | --- |
| Create/update/delete | Primary |
| Read-after-write requiring immediate visibility | Primary |
| Cached or eventually consistent list | Replica |
| Reporting that tolerates lag | Replica |
| Health/lag inspection | Replica and replication metrics |

A common pattern is to pin a user's reads to the primary for a short period
after a write when immediate visibility is required.

## Consistency Trade-off

Read replicas are not a free performance improvement. The system must define
what stale data is acceptable.

Questions to answer:

1. How much lag can the product tolerate?
2. Which endpoints require read-after-write consistency?
3. What happens when every replica exceeds the lag threshold?
4. How are unhealthy replicas removed from routing?
5. How is traffic redistributed during replica failure?

## Monitoring

Useful signals include:

- Replication/replay lag
- Replica CPU and memory
- Replica I/O latency
- Replication backlog
- Read traffic per replica
- Query latency by replica
- Replica availability

A load balancer should not continue routing traffic to a replica that is too far
behind the primary for the consistency requirements of the application.

## Interview Questions

1. Why do read replicas improve read scalability but not write scalability?
2. What is replication lag?
3. How would you handle a read-after-write request with asynchronous replicas?
4. What should happen when all replicas are unhealthy?
5. How would you monitor replication health?
6. When would sharding be a better choice than adding more read replicas?
