-- Day 71 SQL Interview Set 1
-- PostgreSQL-oriented practice. Assume employees, departments, and tasks tables.
-- Try each query before reading the expected approach in the comments.

-- 1. Find employees earning more than 100000, highest salary first.
SELECT employee_id, name, salary
FROM employees
WHERE salary > 100000
ORDER BY salary DESC, employee_id;

-- 2. Return each department and its employee count, including empty departments.
SELECT
    d.department_id,
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN employees AS e
    ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id;

-- 3. Find departments with at least five employees.
SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 5
ORDER BY employee_count DESC, department_id;

-- 4. Find employees earning more than their department's average salary.
SELECT e.employee_id, e.name, e.department_id, e.salary
FROM employees AS e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees AS e2
    WHERE e2.department_id = e.department_id
)
ORDER BY e.department_id, e.salary DESC;

-- 5. Count tasks by status, retaining statuses that have zero tasks when a
-- task_statuses lookup table exists.
-- Assumed task_statuses(status) and tasks(task_id, status) tables.
SELECT
    s.status,
    COUNT(t.task_id) AS task_count
FROM task_statuses AS s
LEFT JOIN tasks AS t
    ON t.status = s.status
GROUP BY s.status
ORDER BY s.status;

-- Interview reminders:
-- WHERE filters rows before grouping; HAVING filters grouped results.
-- COUNT(*) counts joined rows; COUNT(nullable_column) skips NULL values.
-- A LEFT JOIN preserves unmatched rows from the left table.
-- Confirm indexes and execution plans against real data; do not assume a query
-- is fast solely because it is concise.
