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

# Repository Files

sql/
├── README.md
├── aggregate_functions.sql
├── basics.sql
├── constraints.sql
├── ctes.sql
├── indexes.sql
├── joins.sql
├── query_optimization.sql
├── subqueries.sql
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
