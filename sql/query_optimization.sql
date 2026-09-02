-- Query Optimization Examples
-- PostgreSQL

-- Select only the columns required by the application.
SELECT id, title, completed
FROM tasks
WHERE user_id = 10;

-- Index a column frequently used for filtering.
CREATE INDEX idx_tasks_user_id
ON tasks(user_id);

-- Composite index for queries filtering by both columns.
CREATE INDEX idx_tasks_user_completed
ON tasks(user_id, completed);

-- Inspect the query execution plan.
EXPLAIN
SELECT id, title, completed
FROM tasks
WHERE user_id = 10
AND completed = false;

-- Inspect the actual execution plan.
EXPLAIN ANALYZE
SELECT id, title, completed
FROM tasks
WHERE user_id = 10
AND completed = false;

-- Day 13: Query Optimization
-- Topics:
-- EXPLAIN
-- Query Plans
-- Selectivity
-- Index Usage
-- Query Performance

-- ============================================================
-- 1. EXPLAIN
-- ============================================================

-- EXPLAIN shows the execution plan that the database
-- optimizer intends to use for a query.

EXPLAIN
SELECT *
FROM employees
WHERE department_id = 10;


-- ============================================================
-- 2. EXPLAIN ANALYZE
-- ============================================================

-- EXPLAIN ANALYZE executes the query and shows the
-- actual execution statistics.

EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE department_id = 10;


-- ============================================================
-- 3. Query Plan
-- ============================================================

-- A query plan describes how the database intends to
-- retrieve and process the requested data.

-- Common operations include:
-- - Sequential Scan
-- - Index Scan
-- - Index Only Scan
-- - Bitmap Index Scan
-- - Sort
-- - Aggregate
-- - Nested Loop
-- - Hash Join
-- - Merge Join


-- ============================================================
-- 4. Sequential Scan
-- ============================================================

-- A sequential scan reads rows from the table sequentially.

EXPLAIN
SELECT *
FROM employees
WHERE department_id = 10;


-- ============================================================
-- 5. Index Scan
-- ============================================================

-- An index can allow the database to locate matching rows
-- without scanning the entire table.

CREATE INDEX idx_employees_department_id
ON employees(department_id);

EXPLAIN
SELECT *
FROM employees
WHERE department_id = 10;


-- ============================================================
-- 6. Selectivity
-- ============================================================

-- Selectivity describes how effectively a condition
-- narrows down the rows being searched.

-- High selectivity:
-- A condition matches a small percentage of rows.

-- Low selectivity:
-- A condition matches a large percentage of rows.

-- Example of a potentially highly selective column:

CREATE INDEX idx_employees_email
ON employees(email);

EXPLAIN
SELECT *
FROM employees
WHERE email = 'user@example.com';


-- Example of a potentially low-selectivity column:

EXPLAIN
SELECT *
FROM employees
WHERE gender = 'M';


-- ============================================================
-- 7. Avoid SELECT *
-- ============================================================

-- Prefer selecting only the columns required by the application.

-- Less precise:
SELECT *
FROM employees
WHERE department_id = 10;

-- More precise:
SELECT employee_id, name, department_id
FROM employees
WHERE department_id = 10;


-- ============================================================
-- 8. Filtering Early
-- ============================================================

-- Apply filtering conditions that reduce the amount of
-- data processed by the query.

SELECT employee_id, name
FROM employees
WHERE department_id = 10
  AND status = 'active';


-- ============================================================
-- 9. Composite Index
-- ============================================================

-- A composite index can be useful when queries frequently
-- filter using multiple columns.

CREATE INDEX idx_employees_department_status
ON employees(department_id, status);

EXPLAIN
SELECT employee_id, name
FROM employees
WHERE department_id = 10
  AND status = 'active';


-- ============================================================
-- 10. Functions on Indexed Columns
-- ============================================================

-- Applying a function to an indexed column can prevent
-- efficient index usage depending on the database and query.

-- Example:

SELECT *
FROM employees
WHERE LOWER(email) = 'user@example.com';


-- A database-specific functional index or another suitable
-- indexing strategy may be required for efficient execution.


-- ============================================================
-- 11. LIKE and Index Usage
-- ============================================================

-- Prefix searches may be able to use an index depending
-- on the database and collation.

SELECT *
FROM employees
WHERE name LIKE 'John%';


-- Leading wildcards generally make ordinary B-tree indexes
-- less useful.

SELECT *
FROM employees
WHERE name LIKE '%John%';


-- ============================================================
-- 12. ORDER BY and Indexes
-- ============================================================

-- Indexes may also help queries involving ordering,
-- depending on the database and index definition.

CREATE INDEX idx_employees_department_name
ON employees(department_id, name);

EXPLAIN
SELECT employee_id, name
FROM employees
WHERE department_id = 10
ORDER BY name;


-- ============================================================
-- 13. Query Optimization Checklist
-- ============================================================

-- 1. Use EXPLAIN to inspect the query plan.
-- 2. Use EXPLAIN ANALYZE when supported and appropriate.
-- 3. Check whether expensive sequential scans are expected.
-- 4. Check estimated versus actual row counts.
-- 5. Consider appropriate indexes.
-- 6. Consider column selectivity.
-- 7. Avoid unnecessary SELECT *.
-- 8. Filter data as early as practical.
-- 9. Avoid unnecessary functions on indexed columns.
-- 10. Review joins, sorting, and aggregation operations.
-- ============================================================
-- Day 33: Query Plans, Joins and Index Usage
-- ============================================================

-- Read the plan before deciding whether an index or query rewrite
-- is justified. The optimizer chooses a plan from statistics,
-- available indexes, estimated cardinality, and cost.

EXPLAIN
SELECT e.id, e.name, d.name AS department_name
FROM employees AS e
JOIN departments AS d
    ON d.id = e.department_id
WHERE e.status = 'active';


-- Index the join/filter columns when the workload and data
-- distribution justify it.

CREATE INDEX idx_employees_status_department
ON employees(status, department_id);

EXPLAIN
SELECT e.id, e.name, d.name AS department_name
FROM employees AS e
JOIN departments AS d
    ON d.id = e.department_id
WHERE e.status = 'active';


-- A join-column index can help the database locate matching
-- rows efficiently, depending on the chosen join strategy.

CREATE INDEX idx_employees_department_id
ON employees(department_id);

EXPLAIN
SELECT e.id, e.name, d.name AS department_name
FROM departments AS d
JOIN employees AS e
    ON e.department_id = d.id
WHERE d.id = 10;


-- Compare estimated and actual row counts when diagnosing a
-- slow query. Large differences can indicate stale statistics
-- or data-distribution assumptions that need investigation.

EXPLAIN ANALYZE
SELECT e.id, e.name, d.name AS department_name
FROM employees AS e
JOIN departments AS d
    ON d.id = e.department_id
WHERE e.status = 'active';


-- Common join operations visible in PostgreSQL plans include:
-- - Nested Loop
-- - Hash Join
-- - Merge Join
--
-- The fastest join strategy depends on table size, selectivity,
-- available indexes, sort order, and estimated row counts.

-- Day 33 checklist:
-- 1. Read the plan before changing the query.
-- 2. Check estimated versus actual rows.
-- 3. Inspect join strategy and join conditions.
-- 4. Verify indexes on selective filter and join columns.
-- 5. Avoid adding indexes without considering write overhead.
-- 6. Re-measure after each meaningful query or index change.
