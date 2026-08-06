-- ==========================================
-- Window Functions
-- ==========================================

-- Sample Table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary INT
);

INSERT INTO employees VALUES
(1, 'Alice', 'HR', 50000),
(2, 'Bob', 'HR', 60000),
(3, 'Charlie', 'IT', 90000),
(4, 'David', 'IT', 85000),
(5, 'Emma', 'IT', 90000);

-- ==========================================
-- ROW_NUMBER()
-- ==========================================

SELECT
    name,
    salary,
    ROW_NUMBER() OVER (
        ORDER BY salary DESC
    ) AS row_number
FROM employees;

-- ==========================================
-- RANK()
-- ==========================================

SELECT
    name,
    salary,
    RANK() OVER (
        ORDER BY salary DESC
    ) AS employee_rank
FROM employees;

-- ==========================================
-- DENSE_RANK()
-- ==========================================

SELECT
    name,
    salary,
    DENSE_RANK() OVER (
        ORDER BY salary DESC
    ) AS dense_rank
FROM employees;

-- ==========================================
-- PARTITION BY
-- ==========================================

SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS department_rank
FROM employees;

-- ==========================================
-- AVG() as Window Function
-- ==========================================

SELECT
    name,
    salary,
    AVG(salary) OVER () AS average_salary
FROM employees;

-- ==========================================
-- SUM() Running Total
-- ==========================================

SELECT
    id,
    name,
    salary,
    SUM(salary) OVER (
        ORDER BY id
    ) AS running_total
FROM employees;

-- ==========================================
-- COUNT() Window Function
-- ==========================================

SELECT
    name,
    department,
    COUNT(*) OVER (
        PARTITION BY department
    ) AS employees_in_department
FROM employees;

-- ==========================================
-- MAX() Window Function
-- ==========================================

SELECT
    name,
    department,
    salary,
    MAX(salary) OVER (
        PARTITION BY department
    ) AS highest_department_salary
FROM employees;

-- ==========================================
-- MIN() Window Function
-- ==========================================

SELECT
    name,
    department,
    salary,
    MIN(salary) OVER (
        PARTITION BY department
    ) AS lowest_department_salary
FROM employees;