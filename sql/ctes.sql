/*
Common Table Expressions (CTEs)

A CTE is a temporary result set that exists only during the execution
of a single SQL statement.

Syntax

WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
*/


-- Sample Table

CREATE TABLE employees (
    employee_id INT,
    employee_name VARCHAR(50),
    department VARCHAR(50),
    salary INT
);


INSERT INTO employees VALUES
(1, 'Alice', 'Engineering', 80000),
(2, 'Bob', 'Engineering', 75000),
(3, 'Charlie', 'HR', 60000),
(4, 'David', 'Finance', 90000),
(5, 'Eva', 'Engineering', 85000);


-- Basic CTE

WITH engineering_employees AS
(
    SELECT *
    FROM employees
    WHERE department = 'Engineering'
)
SELECT *
FROM engineering_employees;


-- CTE with Aggregate Function

WITH department_salary AS
(
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department
)
SELECT *
FROM department_salary;


-- Multiple CTEs

WITH engineering AS
(
    SELECT *
    FROM employees
    WHERE department = 'Engineering'
),
high_salary AS
(
    SELECT *
    FROM engineering
    WHERE salary > 80000
)
SELECT *
FROM high_salary;