-- Day 72 SQL Interview Set 2: Joins and Grouping
-- PostgreSQL-oriented practice. Assume employees, departments, customers,
-- orders, and order_items tables with the columns referenced below.
-- Try to predict row counts before running each query.

-- 1. List employees with their department names; omit employees without a match.
SELECT
    e.employee_id,
    e.name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON d.department_id = e.department_id
ORDER BY e.employee_id;

-- 2. Return every department, including departments with no employees.
-- COUNT(e.employee_id), unlike COUNT(*), returns zero for an unmatched group.
SELECT
    d.department_id,
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN employees AS e
    ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id;

-- 3. Find departments with at least three employees and their average salary.
SELECT
    d.department_id,
    d.department_name,
    COUNT(e.employee_id) AS employee_count,
    AVG(e.salary) AS average_salary
FROM departments AS d
INNER JOIN employees AS e
    ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
HAVING COUNT(e.employee_id) >= 3
ORDER BY average_salary DESC, d.department_id;

-- 4. Return customers and their order counts, including customers with no orders.
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC, c.customer_id;

-- 5. Calculate total order value per customer. Assume order_items contains
-- quantity and unit_price. Keep only customers with total value above 1000.
SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_order_value
FROM customers AS c
INNER JOIN orders AS o
    ON o.customer_id = c.customer_id
INNER JOIN order_items AS oi
    ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(oi.quantity * oi.unit_price) > 1000
ORDER BY total_order_value DESC, c.customer_id;

-- 6. Count orders by status using conditional aggregation.
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,
    COUNT(o.order_id) FILTER (WHERE o.status = 'completed') AS completed_orders,
    COUNT(o.order_id) FILTER (WHERE o.status = 'cancelled') AS cancelled_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;

-- Interview reminders:
-- * A join can multiply rows when a parent matches multiple child rows.
-- * Put optional-child filters in ON when unmatched parent rows must remain.
-- * WHERE filters rows before grouping; HAVING filters aggregated groups.
-- * COUNT(child.id) excludes NULLs introduced by a LEFT JOIN; COUNT(*) does not.
-- * Avoid selecting non-aggregated columns unless they are grouped or otherwise
--   valid under the SQL dialect's grouping rules.
-- * State assumptions about NULLs, duplicate data, and monetary precision.
