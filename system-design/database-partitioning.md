# Database Partitioning & Sharding

Day 34 focuses on partitioning and sharding as ways to control data size,
query cost, and database capacity as a system grows.

## Partitioning vs Sharding

**Partitioning** splits one logical table into smaller physical partitions,
usually inside the same database system.

**Sharding** distributes partitions across independent database nodes or
clusters.

```text
Partitioning:

             Logical Table
                  |
        +---------+---------+
        |         |         |
      Part A    Part B    Part C
        \         |         /
             One DB

Sharding:

             Logical Dataset
                  |
        +---------+---------+
        |         |         |
      Shard A   Shard B   Shard C
        |         |         |
       DB A      DB B      DB C
```

Partitioning is generally simpler because the database can keep one logical
table abstraction. Sharding adds routing, operational, and cross-node
consistency concerns.

## Partitioning Strategies

### Range Partitioning

Rows are assigned to ranges of a partition key.

Common examples:

- Date ranges
- Numeric ID ranges
- Time-series data

Range partitioning works well when queries commonly filter on the same range
key because irrelevant partitions can be pruned.

### List Partitioning

Rows are grouped by explicit values.

Examples:

- Region
- Tenant tier
- Business unit

### Hash Partitioning

A hash function distributes rows across a fixed number of partitions. It can
provide a more even distribution when the partition key has good cardinality.

## Choosing a Partition Key

A useful partition key should:

1. Match common query filters.
2. Produce a reasonably balanced distribution.
3. Avoid creating a single hot partition.
4. Support predictable data lifecycle operations.
5. Be stable enough that rows do not need frequent movement.

For a time-based Expense Tracker workload, `expense_date` is a natural range
partitioning candidate if the data volume justifies it.

## Partition Pruning

A query against the logical parent can avoid scanning partitions that cannot
contain matching rows.

```text
Query: expense_date = September 2026

             expense_events
                    |
          +---------+---------+
          |         |         |
        Sep 2026  Oct 2026  Nov 2026
          ^
          |
       scanned
```

Pruning is useful only when the query predicate gives the database enough
information to identify relevant partitions.

## Shard Routing

Once data is distributed across database nodes, the application or a routing
layer must determine where a request belongs.

```text
API
 |
 v
Shard Router
 |
 +---- tenant A ----> Shard 1
 +---- tenant B ----> Shard 2
 +---- tenant C ----> Shard 3
```

The routing key should be stable and should avoid concentrating most traffic
on one shard.

## Hot Partitions and Hot Shards

A partition can become a bottleneck even when the total dataset is balanced.
Typical causes include:

- A highly active tenant
- A current time range receiving most writes
- An uneven hash distribution
- A popular query key

Mitigations include better key selection, additional partitioning, workload
isolation, and deliberate traffic distribution.

## Cross-Partition and Cross-Shard Queries

Partitioning inside one database can often preserve familiar SQL semantics.
Sharding makes cross-shard queries more expensive because data must be read
from multiple nodes and combined.

Prefer access patterns that can answer a request from one partition or shard
when possible.

## Operational Considerations

Before introducing partitioning or sharding, define:

- Expected data volume and growth rate
- Query patterns
- Write distribution
- Partition/shard key
- Partition creation and retention process
- Rebalancing strategy
- Backup and restore behavior
- Monitoring and alerting
- Cross-partition/shard query requirements
- Failure and recovery procedures

Partitioning should solve a measured scaling or lifecycle problem rather than
being added solely because a table is large.
