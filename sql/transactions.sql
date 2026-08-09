-- SQL Transactions
-- Demonstrates transaction control using PostgreSQL syntax.

-- COMMIT
-- Changes are permanently saved after COMMIT.

BEGIN;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 101;

COMMIT;


-- ROLLBACK
-- Changes are discarded when ROLLBACK is executed.

BEGIN;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 102;

ROLLBACK;


-- Multiple operations in one transaction

BEGIN;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 103;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 104;

COMMIT;


-- SAVEPOINT
-- Allows partial rollback within a transaction.

BEGIN;

UPDATE employees
SET salary = salary + 2000
WHERE employee_id = 105;

SAVEPOINT salary_update;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 106;

ROLLBACK TO SAVEPOINT salary_update;

COMMIT;