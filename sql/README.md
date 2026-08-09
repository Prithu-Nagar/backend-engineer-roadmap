# SQL

This directory contains practical SQL examples covering database fundamentals, querying, analysis, optimization, and transaction management.

The focus is on writing correct and efficient SQL while understanding how queries interact with relational databases.

---

# Topics

## SQL Basics

Covers fundamental SQL operations including:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `WHERE`
- `ORDER BY`
- `GROUP BY`
- `HAVING`

File: `basics.sql`

---

## Joins

Covers combining data from multiple tables using:

- `INNER JOIN`
- `LEFT JOIN`
- `RIGHT JOIN`
- `FULL OUTER JOIN`

File: `joins.sql`

---

## Aggregate Functions

Covers functions used to perform calculations across rows.

Examples include:

- `COUNT()`
- `SUM()`
- `AVG()`
- `MIN()`
- `MAX()`

---

## Subqueries

Covers queries nested inside other SQL statements.

Topics include:

- Scalar subqueries
- Subqueries with `WHERE`
- Subqueries with `FROM`
- Subqueries with aggregate functions

---

## Common Table Expressions

Covers Common Table Expressions using the `WITH` clause.

CTEs can improve query organization and make complex queries easier to understand.

File: `ctes.sql`

---

## Window Functions

Covers analytical functions that operate across related rows without collapsing the result set.

Examples include:

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `LAG()`
- `LEAD()`

File: `window_functions.sql`

---

## Indexes

Covers database indexes and how they can improve query performance.

Topics include:

- Index purpose
- Index creation
- Index usage
- Index trade-offs
- Read vs write performance

File: `indexes.sql`

---

## Query Optimization

Covers techniques for understanding and improving SQL query performance.

Topics include:

- Execution plans
- `EXPLAIN`
- Index usage
- Avoiding unnecessary scans
- Query performance analysis

File: `query_optimization.sql`

---

## Transactions

Covers maintaining consistency across multiple database operations.

Topics include:

- `BEGIN`
- `COMMIT`
- `ROLLBACK`
- `SAVEPOINT`
- Atomic operations

File: `transactions.sql`

---

# Repository Structure

sql/
├── README.md
├── basics.sql
├── joins.sql
├── aggregate_functions.sql
├── subqueries.sql
├── ctes.sql
├── window_functions.sql
├── indexes.sql
├── query_optimization.sql
└── transactions.sql

---

# Completed Topics

- SQL Basics
- Joins
- Aggregate Functions
- Subqueries
- Common Table Expressions
- Window Functions
- Indexes
- Query Optimization
- Transactions

---

# Upcoming Topics

- Advanced Query Optimization
- Database Design
- Normalization

---

# Learning Approach

For each SQL topic:

1. Understand the underlying database concept.
2. Write practical SQL examples.
3. Analyze query behavior.
4. Consider performance implications.
5. Understand how indexes and execution plans affect queries.
6. Apply transaction and consistency concepts to backend applications.
