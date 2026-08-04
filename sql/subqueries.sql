-- Single Row Subquery

SELECT *
FROM Employees
WHERE salary >
(
    SELECT AVG(salary)
    FROM Employees
);


-- Multiple Row Subquery

SELECT *
FROM Employees
WHERE department_id IN
(
    SELECT department_id
    FROM Departments
    WHERE city = 'Delhi'
);


-- Correlated Subquery

SELECT e.employee_name,
       e.salary
FROM Employees e
WHERE salary >
(
    SELECT AVG(salary)
    FROM Employees
    WHERE department_id = e.department_id
);


-- EXISTS

SELECT *
FROM Customers c
WHERE EXISTS
(
    SELECT 1
    FROM Orders o
    WHERE o.customer_id = c.customer_id
);


-- NOT EXISTS

SELECT *
FROM Customers c
WHERE NOT EXISTS
(
    SELECT 1
    FROM Orders o
    WHERE o.customer_id = c.customer_id
);