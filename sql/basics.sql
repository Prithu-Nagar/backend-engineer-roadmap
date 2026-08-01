-- SELECT

SELECT *
FROM Employee;

-- WHERE

SELECT *
FROM Employee
WHERE salary > 50000;

-- ORDER BY

SELECT *
FROM Employee
ORDER BY salary DESC;

-- GROUP BY

SELECT department,
COUNT(*)
FROM Employee
GROUP BY department;

-- HAVING

SELECT department,
COUNT(*)
FROM Employee
GROUP BY department
HAVING COUNT(*) > 5;

-- DISTINCT

SELECT DISTINCT department
FROM Employee;

-- IS NULL

SELECT *
FROM Employee
WHERE manager_id IS NULL;