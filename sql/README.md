# SQL

This directory contains SQL concepts and practical query examples covered throughout the Backend Engineer Roadmap.

The goal is to build strong SQL fundamentals required for backend development, database interaction, performance optimization, data integrity, and technical interviews.

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

WITH high_value_orders AS (
    SELECT *
    FROM orders
    WHERE amount > 1000
)
SELECT *
FROM high_value_orders;

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

# Repository Files

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
