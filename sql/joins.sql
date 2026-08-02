-- INNER JOIN

SELECT e.employee_name,
       d.department_name
FROM Employee e
INNER JOIN Department d
ON e.department_id = d.department_id;


-- LEFT JOIN

SELECT e.employee_name,
       d.department_name
FROM Employee e
LEFT JOIN Department d
ON e.department_id = d.department_id;


-- RIGHT JOIN

SELECT e.employee_name,
       d.department_name
FROM Employee e
RIGHT JOIN Department d
ON e.department_id = d.department_id;


-- FULL OUTER JOIN

SELECT e.employee_name,
       d.department_name
FROM Employee e
FULL OUTER JOIN Department d
ON e.department_id = d.department_id;


-- CROSS JOIN

SELECT e.employee_name,
       d.department_name
FROM Employee e
CROSS JOIN Department d;


-- SELF JOIN

SELECT e.employee_name,
       m.employee_name AS manager_name
FROM Employee e
LEFT JOIN Employee m
ON e.manager_id = m.employee_id;