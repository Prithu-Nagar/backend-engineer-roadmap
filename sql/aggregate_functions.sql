-- ============================================
-- Aggregate Functions Practice
-- ============================================

CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(30),
    salary INT
);

INSERT INTO Employee VALUES
(1,'Alice','IT',70000),
(2,'Bob','IT',85000),
(3,'Charlie','HR',50000),
(4,'David','Finance',90000),
(5,'Eva','HR',60000),
(6,'Frank','IT',95000),
(7,'Grace','Finance',75000);

-- ============================================
-- COUNT
-- ============================================

SELECT COUNT(*) AS total_employees
FROM Employee;

-- ============================================
-- SUM
-- ============================================

SELECT SUM(salary) AS total_salary
FROM Employee;

-- ============================================
-- AVG
-- ============================================

SELECT AVG(salary) AS average_salary
FROM Employee;

-- ============================================
-- MIN
-- ============================================

SELECT MIN(salary) AS minimum_salary
FROM Employee;

-- ============================================
-- MAX
-- ============================================

SELECT MAX(salary) AS maximum_salary
FROM Employee;

-- ============================================
-- DISTINCT
-- ============================================

SELECT DISTINCT department
FROM Employee;

-- ============================================
-- GROUP BY
-- ============================================

SELECT
    department,
    COUNT(*) AS employee_count
FROM Employee
GROUP BY department;

-- ============================================
-- Average salary department-wise
-- ============================================

SELECT
    department,
    AVG(salary) AS average_salary
FROM Employee
GROUP BY department;

-- ============================================
-- Maximum salary department-wise
-- ============================================

SELECT
    department,
    MAX(salary) AS highest_salary
FROM Employee
GROUP BY department;

-- ============================================
-- HAVING
-- ============================================

SELECT
    department,
    COUNT(*) AS total_employees
FROM Employee
GROUP BY department
HAVING COUNT(*) >= 2;

-- ============================================
-- HAVING with AVG
-- ============================================

SELECT
    department,
    AVG(salary) AS average_salary
FROM Employee
GROUP BY department
HAVING AVG(salary) > 70000;