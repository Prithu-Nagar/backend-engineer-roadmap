-- Day 73 SQL Interview Set 3: Window Functions and CTEs
-- PostgreSQL-oriented practice. Assume employees, departments, orders, and
-- customers tables with the columns referenced below.
-- Run each query independently and explain ties, NULL handling, and row grain.

-- 1. Rank employees by salary within each department. Ties share a rank.
SELECT
    employee_id,
    department_id,
    name,
    salary,
    RANK() OVER (
        PARTITION BY department_id
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees
ORDER BY department_id, salary_rank, employee_id;

-- 2. Return the two highest-paid employees per department.
-- ROW_NUMBER chooses exactly two rows when a department has at least two.
WITH ranked_employees AS (
    SELECT
        employee_id,
        department_id,
        name,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC, employee_id
        ) AS row_num
    FROM employees
)
SELECT employee_id, department_id, name, salary
FROM ranked_employees
WHERE row_num <= 2
ORDER BY department_id, row_num;

-- 3. Compare each employee's salary with the previous salary in their department.
SELECT
    employee_id,
    department_id,
    name,
    salary,
    LAG(salary) OVER (
        PARTITION BY department_id
        ORDER BY salary, employee_id
    ) AS previous_salary,
    salary - LAG(salary) OVER (
        PARTITION BY department_id
        ORDER BY salary, employee_id
    ) AS salary_difference
FROM employees
ORDER BY department_id, salary, employee_id;

-- 4. Calculate a running total of each customer's order amount.
SELECT
    customer_id,
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders
ORDER BY customer_id, order_date, order_id;

-- 5. Use a CTE to calculate customer spend, then filter aggregate results.
WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(total_amount) AS lifetime_spend,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, lifetime_spend, order_count
FROM customer_spend
WHERE lifetime_spend >= 1000
ORDER BY lifetime_spend DESC, customer_id;

-- 6. Find each department's average salary and employees above that average.
WITH department_averages AS (
    SELECT department_id, AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    e.employee_id,
    e.name,
    e.department_id,
    e.salary,
    d.average_salary
FROM employees AS e
JOIN department_averages AS d
    ON d.department_id = e.department_id
WHERE e.salary > d.average_salary
ORDER BY e.department_id, e.salary DESC, e.employee_id;

-- Review prompts:
-- * RANK vs DENSE_RANK vs ROW_NUMBER: how do ties affect results?
-- * Why should window ORDER BY include a deterministic tie-breaker?
-- * How do NULL values affect ranking and aggregates?
-- * When does a CTE improve clarity, and when should you inspect the query plan?
