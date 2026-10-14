# Database Scaling — Mock Interview

Use this mock interview to practice a structured approach to scaling a relational database. State assumptions, identify bottlenecks with evidence, and explain trade-offs before choosing a solution.

## Scenario

A task-management API has grown from a small internal tool to a high-traffic service. Read latency is increasing, writes are slowing during peak periods, and the primary database is consuming most of its available CPU and I/O capacity.

## 1. Clarify Requirements

Ask about:

- Read/write ratio and peak requests per second.
- Dataset size, growth rate, and query patterns.
- Latency targets and availability objectives.
- Consistency requirements for task creation, updates, and reads.
- Current database engine, indexes, connection pool, and deployment topology.
- Backup, recovery, and data-retention requirements.

Do not assume that traffic volume alone proves the database needs sharding.

## 2. Establish the Baseline

Inspect query latency percentiles, slow-query logs, execution plans, lock waits, connection saturation, cache hit rates, disk I/O, CPU, replication lag, and pool wait time. Separate application latency from database execution time.

## 3. Choose the Least Complex Effective Change

1. Fix inefficient queries and missing or unsuitable indexes.
2. Bound application connection pools and eliminate connection leaks.
3. Cache suitable read-heavy data with explicit TTL and invalidation behavior.
4. Add read replicas when read traffic is the bottleneck and replica staleness is acceptable.
5. Partition large tables when partition pruning or maintenance benefits justify the complexity.
6. Consider sharding only when a single database cannot meet requirements after measured optimizations.

## 4. Discuss the Trade-offs

### Read Replicas
- Benefit: distribute eligible reads and improve read capacity.
- Risks: replication lag, stale reads, routing complexity, and failover considerations.
- Mitigation: route consistency-sensitive reads to the primary and monitor lag.

### Partitioning
- Benefit: manage large tables and potentially reduce work for queries aligned with the partition key.
- Risks: poor partition-key choice, operational overhead, and queries that cannot prune partitions.
- Mitigation: validate query plans and operational requirements with representative data.

### Sharding
- Benefit: distribute storage and write load across database nodes.
- Risks: cross-shard queries, transactions, rebalancing, hot shards, and more complex operations.
- Mitigation: choose a stable shard key, plan resharding, and define cross-shard consistency expectations.

## 5. Failure and Recovery Questions

- What happens if a read replica falls behind or becomes unavailable?
- How are primary failover and connection recovery handled?
- How do you prevent cache stampedes during a cold start?
- How do backups and point-in-time recovery meet the recovery objectives?
- How would you roll out a partitioning or sharding change safely?

## 6. Success Criteria

Define measurable outcomes before implementation: query latency percentiles, throughput, error rate, database saturation, pool wait time, replication lag, and recovery time. Compare results under the same representative workload and revisit the design if the original bottleneck remains.

## Interview Closing Summary

Start with evidence, optimize queries and connection usage, add replicas or caching when their consistency trade-offs are acceptable, and introduce partitioning or sharding only when justified by measured scale. Explain operational cost and failure behavior alongside capacity gains.
