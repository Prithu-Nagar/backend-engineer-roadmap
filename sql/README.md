# SQL

This directory contains SQL concepts and practical query examples covered throughout the Backend Engineer Roadmap.

The goal is to build strong SQL fundamentals required for backend development, database interaction, performance optimization, data integrity, and technical interviews.

---

## Day 19 — Practical Transactions

Day 19 extends the existing transaction material with practical
business scenarios.

Scenarios include:

- Bank transfers
- Rollback after failure
- SAVEPOINT usage
- Multi-step order creation
- Inventory updates
- Concurrent inventory updates
- SELECT ... FOR UPDATE
- Explicit transaction isolation

File:

`transactions.sql`

The focus is on identifying transaction boundaries around real
business operations rather than treating transactions as isolated SQL syntax.

---

## Completed Topics

- SQL Basics
- Joins
- Aggregate Functions
- Subqueries
- Indexes
- Window Functions
- Common Table Expressions (CTEs)
- Query Optimization
- Transactions
- Transaction control and isolation levels
- Constraints
- Covering indexes
- PostgreSQL `INCLUDE` columns
- Index-only scan concept
- Database Normalization

---

## Current Topics

None

---

## Upcoming Topics

- Advanced Database Design
- Database Scaling
- Advanced Query Optimization

---

# Topics

## SQL Basics

Covers fundamental SQL operations including:

- SELECT
- INSERT
- UPDATE
- DELETE
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- DISTINCT
- LIMIT

**File:** `basics.sql`

---

## Joins

Covers combining data from multiple tables.

Topics include:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- SELF JOIN

**File:** `joins.sql`

---

## Aggregate Functions

Covers SQL functions used to calculate values across multiple rows.

Examples include:

- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()
- GROUP BY
- HAVING

**File:** `aggregate_functions.sql`

---

## Subqueries

Covers queries nested inside other SQL queries.

Topics include:

- Scalar subqueries
- Subqueries with WHERE
- Subqueries with IN
- Correlated subqueries
- EXISTS

**File:** `subqueries.sql`

---

## Indexes

Indexes improve the performance of database queries by providing a faster way to locate rows.

Topics include:

- Basic indexes
- Unique indexes
- Composite indexes
- Index column order
- EXPLAIN
- EXPLAIN ANALYZE
- Index trade-offs

**File:** `indexes.sql`

---

## Window Functions

Window functions perform calculations across a set of related rows without collapsing them into a single row.

Common examples include:

- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- LAG()
- LEAD()
- PARTITION BY
- ORDER BY

**File:** `window_functions.sql`

---

## Common Table Expressions (CTEs)

CTEs allow complex queries to be broken into named temporary result sets.

Example:

```sql
WITH high_value_orders AS (
    SELECT *
    FROM orders
    WHERE amount > 1000
)
SELECT *
FROM high_value_orders;
```

**File:** `ctes.sql`

---

## Query Optimization

Covers techniques for understanding and improving SQL query performance.

Topics include:

- Selecting only required columns
- Filtering efficiently
- Index usage
- Composite indexes
- EXPLAIN
- EXPLAIN ANALYZE
- Query execution plans
- Avoiding unnecessary scans
- Matching indexes to read patterns

**File:** `query_optimization.sql`

Example patterns include reduced result sets, index-friendly predicates, and using execution plans to confirm where the database is spending time.

---

## Transactions

Transactions allow multiple database operations to be treated as a single unit of work.

Topics include:

- COMMIT
- ROLLBACK
- Atomicity
- Consistency
- Isolation
- Durability
- Transaction boundaries

**File:** `transactions.sql`

---

## Constraints

Constraints enforce data integrity at the database level.

Topics include:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT
- Referential integrity
- Parameterized queries

**File:** `constraints.sql`

The examples demonstrate how database constraints can prevent invalid data and enforce relationships between tables.

Parameterized queries should be used by application code rather than constructing SQL statements through string concatenation.

---

## Database Normalization

Day 15 introduces database normalization and schema design.

Database normalization is the process of organizing database design to minimize redundancy and dependency anomalies while maintaining data integrity.

Topics include:

- Normalization forms (1NF, 2NF, 3NF, BCNF)
- Atomic values
- Repeating groups
- Partial dependencies
- Transitive dependencies
- Normalization benefits
- Trade-offs: normalization vs. denormalization
- Schema design best practices
- Foreign key relationships

**File:** `normalization.sql`

Normalization levels:

- **1NF (First Normal Form):** Remove repeating groups, ensure atomic values
- **2NF (Second Normal Form):** 1NF + No partial dependencies (depends only on primary key)
- **3NF (Third Normal Form):** 2NF + No transitive dependencies (no non-key fields depend on other non-key fields)
- **BCNF (Boyce-Codd Normal Form):** 3NF with additional constraints (every determinant is a candidate key)

The examples include normalized schema designs for e-commerce systems and queries on those normalized schemas.

---

## Pagination

Pagination
OFFSET pagination
Keyset/cursor pagination
Stable ordering

**File:** `pagination.sql`

---

### Day 18 — SQL Interview Patterns

Day 18 focuses on common interview query patterns:

- Top-N records
- Top-N per group
- Latest row
- Latest row per group
- Duplicate detection
- Duplicate rows

Important techniques include:

- ORDER BY + LIMIT
- ROW_NUMBER()
- PARTITION BY
- GROUP BY
- HAVING

---

## Day 22 — Django ORM Basics

Day 22 introduces Django's ORM as the application-facing layer for relational
database access.

Topics include:

- Django models
- Model fields
- QuerySets
- Filtering
- Creating records
- Updating records
- Deleting records
- QuerySet laziness
- ORM vs raw SQL trade-offs

File:

`django_orm_basics.md`

The ORM maps Python model operations to SQL while keeping database access
closely connected to application domain models.

---

# Repository Files

```text
sql/
├── README.md
├── aggregate_functions.sql
├── basics.sql
├── constraints.sql
├── ctes.sql
├── indexes.sql
├── joins.sql
├── normalization.sql
├── query_optimization.sql
├── subqueries.sql
├── transactions.sql
└── window_functions.sql
```

---

# Learning Progress

| Topic               | Status    |
| ------------------- | --------- |
| SQL Basics          | Completed |
| Joins               | Completed |
| Aggregate Functions | Completed |
| Subqueries          | Completed |
| Indexes             | Completed |
| Window Functions    | Completed |
| CTEs                | Completed |
| Query Optimization  | Completed |
| Transactions        | Completed |
| Constraints         | Completed |
| Normalization       | Completed |

---

# Learning Strategy

For each SQL topic:

1. Understand the underlying concept.
2. Study the syntax.
3. Write practical queries.
4. Understand query performance.
5. Understand data integrity and database constraints.
6. Practice interview-oriented problems.
7. Apply the concept to backend database operations.

The goal is to understand not only how to write SQL queries, but also how those queries behave in real backend applications.

---

## Day 23 — Django ORM Querying

Day 23 extends Django ORM fundamentals into related-object querying and
query-count awareness.

Topics include:

- Related-object querying
- `select_related()`
- `prefetch_related()`
- N+1 query patterns
- Query composition
- Choosing eager-loading strategies

File:

`django_orm_querying.md`

The goal is to make ORM code convenient without accidentally turning one API
request into a large number of database queries.

---

## Day 24 — ORM Performance

Day 24 focuses on performance issues that can be hidden behind ORM
abstractions.

Topics include:

- N+1 query detection
- `select_related()`
- `prefetch_related()`
- Query-count awareness
- Relationship loading trade-offs
- Inspecting generated SQL

Detailed notes:

`django_orm_querying.md`

## Day 25 — Django ORM Transactions

Day 25 applies transaction concepts through Django's ORM.

Topics include:

- `transaction.atomic()`
- Commit and rollback behavior
- Nested atomic blocks and savepoints
- `select_for_update()`
- Short transaction boundaries
- Concurrency and lock considerations

Detailed notes:

`django_orm_transactions.md`

The focus is on keeping related database writes consistent while avoiding
unnecessarily long transactions.

---

## Day 26 — Indexing in Django & Relational Databases

Day 26 connects relational-database indexing with Django model configuration.

Topics include:

- `db_index=True`
- Django `Meta.indexes`
- Composite indexes
- Index column order
- Query planner inspection with `EXPLAIN`
- Django `QuerySet.explain()`
- Read-performance vs write/storage trade-offs

Detailed notes:

`django_indexes.md`

---

## Day 27 — PostgreSQL JSON Fields

Day 27 introduces PostgreSQL-oriented features, with a focus on JSON and JSONB
for structured but flexible attributes.

Topics include:

- `JSONB`
- JSON field extraction
- JSON containment with `@>`
- JSON array membership
- `jsonb_set()` updates
- GIN indexing for JSONB
- Relational columns vs flexible JSON attributes

Detailed examples:

`postgresql_json_fields.sql`

JSONB should complement relational modeling rather than replace strongly typed
columns that require frequent joins, constraints, or conventional indexes.

---

## Day 28 — Advanced Pagination & Query Patterns

Day 28 extends pagination from the earlier API work into database-oriented
query design.

Topics include:

- Stable ordering
- Composite cursors
- Keyset/cursor pagination
- Filtering before pagination
- Count-query trade-offs
- Parameterized query values
- Allowlisting sort fields
- Indexing for common pagination patterns

Detailed examples:

`pagination.sql`

The goal is to keep pagination predictable and efficient as datasets grow,
while avoiding unsafe dynamic SQL construction.

---

## Day 29 — Database Migration Strategy & Backward-Compatible Schema Changes

Day 29 focuses on evolving relational schemas safely while multiple application
versions may coexist.

Topics include:

- Version-controlled migrations
- Expand-and-contract strategy
- Backward-compatible schema changes
- Safe column additions and removals
- Data backfills
- Constraint rollout
- Rolling-deployment compatibility

Detailed notes:

`migrations.md`

The goal is to make schema changes incrementally without breaking existing
application instances or consumers.

---

## Day 30 — SQL Review

Day 30 reviews the database concepts covered during Days 11–29.

Review areas:

- Transactions and atomicity
- Isolation and concurrency considerations
- Indexes and query-planner awareness
- Normalization and relational modeling
- Query optimization
- ORM vs raw SQL trade-offs
- Pagination and query patterns
- Migration-safe schema changes

The review connects individual SQL techniques to backend application behavior:
correctness, performance, maintainability, and safe schema evolution.

---

## Day 31 — Transaction Isolation Levels

Day 31 focuses on how transaction isolation affects concurrent database work.

Topics include:

- `READ UNCOMMITTED`
- `READ COMMITTED`
- `REPEATABLE READ`
- `SERIALIZABLE`
- Dirty reads
- Non-repeatable reads
- Phantom reads
- Stable transaction snapshots
- Isolation vs concurrency trade-offs

Detailed examples:

`isolation_levels.sql`

The examples are PostgreSQL-oriented. In PostgreSQL, `READ UNCOMMITTED`
behaves like `READ COMMITTED`, so dirty reads are not exposed.

---

## Day 32 — Deadlocks: Detection & Avoidance

Day 32 focuses on deadlocks that can occur when concurrent transactions hold
resources while waiting for resources held by each other.

Topics include:

- Deadlock cycles
- Consistent lock ordering
- Transaction scope
- PostgreSQL lock inspection
- Lock and statement timeouts
- Retry handling for safe operations

Detailed examples:

`deadlocks.sql`

The examples are PostgreSQL-oriented and include two-session deadlock
scenarios plus practical avoidance and observability queries.

---

## Day 33 — Query Plans, Joins & Index Usage

Day 33 applies query-plan reading to joins and index selection.

Topics include:

- `EXPLAIN`
- Estimated rows and cost
- Join strategies
- Index scans
- Composite indexes
- Join-column indexes
- Filtering before expensive operations
- Comparing plans rather than assuming an index is always beneficial

Detailed examples:

`query_optimization.sql`

The examples are PostgreSQL-oriented. Query plans should be measured with the
actual schema and data distribution because the optimizer may choose different
strategies as cardinality and statistics change.

---

## Day 34 — Database Partitioning

Day 34 introduces database partitioning as a way to divide a large logical
table into smaller physical partitions.

Topics include:

- Range partitioning
- List and hash partitioning concepts
- Partition pruning
- Partition-local indexes
- Default partitions
- Partition lifecycle management
- Partitioning vs sharding

Detailed examples:

`partitioning.sql`

The examples are PostgreSQL-oriented and use time-based range partitioning to
illustrate how date-filtered queries can avoid irrelevant partitions.

---

## Day 35 — Read Replicas & Replication Lag

Day 35 introduces read replicas as a way to scale read-heavy database
workloads while accounting for asynchronous replication lag.

Topics include:

- Primary and read-replica roles
- Read/write splitting
- Eventual consistency
- Read-after-write consistency
- Replication/replay lag
- Replica health and routing
- Fallback to the primary when consistency requirements demand it

Detailed examples:

`read_replicas.sql`

The examples are PostgreSQL-oriented and focus on the application-level
trade-off between read scalability and replica freshness.

---

## Day 36 — Full-Text Search

Day 36 introduces PostgreSQL full-text search for linguistic search over text
such as expense descriptions.

Topics include:

- `tsvector`
- `tsquery`
- `to_tsvector()`
- `plainto_tsquery()`
- `to_tsquery()`
- GIN indexes
- `ts_rank()`
- Search configuration and indexing trade-offs

Detailed examples:

`full_text_search.sql`

The examples use the existing Expense Tracker `category` and `description`
fields and demonstrate both search and relevance ranking.
