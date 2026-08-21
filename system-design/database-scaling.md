# Database Scaling

As traffic and data volume increase, the database can become a bottleneck.

## Common Approaches

### Vertical Scaling

Increase the resources of the existing database server.

```text
Database
   ↓
More CPU
More RAM
More Storage
```

### Read Replicas

Distribute read traffic across replica databases while writes are handled by the primary.

```text
             Application
             /         \
         Writes        Reads
            ↓            ↓
         Primary      Replicas
```

### Replication

Maintain additional copies of database data for availability and read scalability.

A key consideration is **replication lag**, where replicas may temporarily be behind the primary.

### Partitioning

Split a large table into smaller partitions based on a partition key.

### Sharding

Distribute data across multiple database nodes.

```text
Application
     ↓
Shard Router
   /  |  \
 S1  S2  S3
```

## Scaling Principle

```text
Measure
   ↓
Identify Bottleneck
   ↓
Optimize
   ↓
Scale When Necessary
```

The appropriate strategy depends on the application's workload, consistency requirements, and bottleneck.
