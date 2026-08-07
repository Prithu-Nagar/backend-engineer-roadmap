# SQL

This directory contains SQL concepts and practical query examples covered throughout the Backend Engineer Roadmap.

The goal is to build strong SQL fundamentals required for backend development, database interaction, and technical interviews.

---

## Completed Topics

- SQL Basics
- Joins
- Aggregate Functions
- Subqueries
- Indexes

---

## Current Topics

- Window Functions

---

## Upcoming Topics

- Common Table Expressions (CTEs)
- Transactions
- Query Optimization

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

# Repository Files


sql/
├── README.md
├── basics.sql
├── joins.sql
├── aggregate_functions.sql
├── subqueries.sql
├── indexes.sql
├── window_functions.sql
└── ctes.sql

---

# Learning Progress

| Topic               | Status      |
| ------------------- | ----------- |
| SQL Basics          | Completed   |
| Joins               | Completed   |
| Aggregate Functions | Completed   |
| Subqueries          | Completed   |
| Indexes             | Completed   |
| Window Functions    | In Progress |
| CTEs                | Upcoming    |
| Transactions        | Upcoming    |
| Query Optimization  | Upcoming    |

---

# Learning Strategy

For each SQL topic:

1. Understand the underlying concept.
2. Study the syntax.
3. Write practical queries.
4. Understand query performance.
5. Practice interview-oriented problems.
6. Apply the concept to backend database operations.

The goal is to understand not only how to write SQL queries, but also how those queries behave in real backend applications.

