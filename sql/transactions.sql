-- SQL Transactions
-- Demonstrates transaction control, ACID properties,
-- isolation levels, and row-level locking using PostgreSQL syntax.

-- ============================================================
-- ACID PROPERTIES
-- ============================================================

-- Atomicity
-- A transaction is treated as a single unit of work.
-- Either all operations succeed or the transaction is rolled back.

BEGIN;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 101;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 102;

COMMIT;

-- Consistency
-- A transaction should move the database from one valid state
-- to another valid state while respecting database constraints.
----------------------------------------------------------------

-- Example:
-- An UPDATE that violates a database constraint should fail
-- rather than leaving the database in an invalid state.

-- Isolation
-- Concurrent transactions should not incorrectly interfere
-- with one another.
--------------------

## -- PostgreSQL provides multiple transaction isolation levels:

-- READ UNCOMMITTED
-- READ COMMITTED
-- REPEATABLE READ
-- SERIALIZABLE

-- Durability
-- Once a transaction has been successfully committed,
-- its changes are persisted by the database.

-- ============================================================
-- COMMIT
-- ============================================================

-- Changes are permanently saved after COMMIT.

BEGIN;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 101;

COMMIT;

-- ============================================================
-- ROLLBACK
-- ============================================================

-- Changes are discarded when ROLLBACK is executed.

BEGIN;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 102;

ROLLBACK;

-- ============================================================
-- MULTIPLE OPERATIONS IN ONE TRANSACTION
-- ============================================================

BEGIN;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 103;

UPDATE employees
SET salary = salary + 3000
WHERE employee_id = 104;

COMMIT;

-- ============================================================
-- SAVEPOINT
-- ============================================================

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

-- ============================================================
-- TRANSACTION ISOLATION LEVELS
-- ============================================================

## -- PostgreSQL supports the following isolation levels:

-- READ UNCOMMITTED
-- READ COMMITTED
-- REPEATABLE READ
-- SERIALIZABLE
---------------

-- READ COMMITTED is PostgreSQL's default isolation level.

-- READ COMMITTED

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT *
FROM employees
WHERE employee_id = 101;

COMMIT;

-- REPEATABLE READ

BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT *
FROM employees
WHERE employee_id = 101;

COMMIT;

-- SERIALIZABLE

BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT *
FROM employees
WHERE employee_id = 101;

COMMIT;

## -- READ UNCOMMITTED

## -- PostgreSQL treats READ UNCOMMITTED as READ COMMITTED.

-- The following syntax is valid PostgreSQL syntax, but it
-- provides READ COMMITTED behavior.

BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

SELECT *
FROM employees
WHERE employee_id = 101;

COMMIT;

-- ============================================================
-- WHY ISOLATION LEVELS MATTER
-- ============================================================

-- Isolation levels control how concurrent transactions can
-- observe changes made by other transactions.
----------------------------------------------

## -- Important concurrency problems include:

-- Dirty Read
-- Non-repeatable Read
-- Phantom Read
---------------

-- Higher isolation generally provides stronger consistency
-- guarantees but can reduce concurrency.

-- ============================================================
-- ROW-LEVEL LOCKING
-- ============================================================

## -- SELECT ... FOR UPDATE obtains a row-level lock.

-- This is useful when a transaction needs to read a row and
-- then safely modify it without another transaction modifying
-- the same row first.

BEGIN;

SELECT *
FROM employees
WHERE employee_id = 101
FOR UPDATE;

UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 101;

COMMIT;

-- ============================================================
-- SELECT FOR UPDATE
-- ============================================================

## -- The selected rows remain locked until the transaction ends.

-- Another transaction attempting to update the same locked row
-- may have to wait until the first transaction commits or rolls
-- back.

BEGIN;

SELECT *
FROM employees
WHERE employee_id = 102
FOR UPDATE;

UPDATE employees
SET salary = salary + 2000
WHERE employee_id = 102;

COMMIT;

-- ============================================================
-- LOCKING AND CONCURRENT UPDATES
-- ============================================================

## -- Example scenario:

## -- Transaction A:

-- BEGIN;
-- SELECT *
-- FROM employees
-- WHERE employee_id = 103
-- FOR UPDATE;
--------------

-- Transaction B attempting to update employee 103 may need
-- to wait until Transaction A finishes.
----------------------------------------

## -- Transaction A:

## -- COMMIT;

-- The lock is then released.

-- ============================================================
-- TRANSACTION REVISION
-- ============================================================

-- BEGIN
--     Starts a transaction.
----------------------------

-- COMMIT
--     Permanently saves the transaction's changes.
---------------------------------------------------

-- ROLLBACK
--     Discards changes made during the transaction.
----------------------------------------------------

-- SAVEPOINT
--     Creates a point to which the transaction can partially
--     roll back.
-----------------

-- ACID
--     Atomicity
--     Consistency
--     Isolation
--     Durability
-----------------

-- Isolation Levels
--     READ UNCOMMITTED
--     READ COMMITTED
--     REPEATABLE READ
--     SERIALIZABLE
-------------------

-- Locks
--     Protect rows from conflicting concurrent modifications.
--------------------------------------------------------------

-- SELECT ... FOR UPDATE
--     Locks selected rows for update until the transaction ends.

-- ============================================================
-- DAY 19 - PRACTICAL TRANSACTION SCENARIOS
-- ============================================================

-- ============================================================
-- SCENARIO 1: BANK TRANSFER
-- ============================================================
-- A transfer should debit one account and credit another
-- atomically.
--
-- If either operation fails, the entire transaction should
-- be rolled back.

BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 101;

UPDATE accounts
SET balance = balance + 1000
WHERE account_id = 202;

COMMIT;


-- ============================================================
-- SCENARIO 2: BANK TRANSFER WITH ROLLBACK
-- ============================================================
-- If validation or another operation fails, rollback prevents
-- a partial transfer.

BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 101;

-- Example validation failure:
-- The destination account does not exist.

UPDATE accounts
SET balance = balance + 1000
WHERE account_id = 999999;

-- Roll back the debit as well.
ROLLBACK;


-- ============================================================
-- SCENARIO 3: SAVEPOINT
-- ============================================================
-- SAVEPOINT allows part of a transaction to be undone while
-- preserving earlier successful operations.

BEGIN;

UPDATE orders
SET status = 'PROCESSING'
WHERE order_id = 1001;

SAVEPOINT before_shipping_update;

UPDATE orders
SET shipping_address = 'Temporary Address'
WHERE order_id = 1001;

-- Suppose the address validation fails.
ROLLBACK TO SAVEPOINT before_shipping_update;

-- The order status update remains,
-- but the shipping address change is undone.

COMMIT;


-- ============================================================
-- SCENARIO 4: MULTI-STEP ORDER CREATION
-- ============================================================
-- Creating an order may involve multiple related operations.

BEGIN;

INSERT INTO orders (
    order_id,
    customer_id,
    status
)
VALUES (
    5001,
    101,
    'CREATED'
);

INSERT INTO order_items (
    order_id,
    product_id,
    quantity
)
VALUES (
    5001,
    301,
    2
);

UPDATE inventory
SET quantity = quantity - 2
WHERE product_id = 301;

COMMIT;


-- ============================================================
-- SCENARIO 5: ORDER CREATION FAILURE
-- ============================================================
-- If inventory update fails, the order should not remain
-- partially created.

BEGIN;

INSERT INTO orders (
    order_id,
    customer_id,
    status
)
VALUES (
    5002,
    101,
    'CREATED'
);

INSERT INTO order_items (
    order_id,
    product_id,
    quantity
)
VALUES (
    5002,
    302,
    5
);

-- Example:
-- inventory constraint or business validation fails.

UPDATE inventory
SET quantity = quantity - 5
WHERE product_id = 302;

-- If the operation cannot be completed safely:
ROLLBACK;


-- ============================================================
-- SCENARIO 6: SAFE CONCURRENT INVENTORY UPDATE
-- ============================================================
-- SELECT FOR UPDATE can prevent two concurrent transactions
-- from modifying the same inventory row simultaneously.

BEGIN;

SELECT quantity
FROM inventory
WHERE product_id = 301
FOR UPDATE;

UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 301
  AND quantity > 0;

COMMIT;


-- ============================================================
-- SCENARIO 7: EXPLICIT TRANSACTION ISOLATION
-- ============================================================
-- Use a stronger isolation level when the business operation
-- requires stronger consistency guarantees.

BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT *
FROM accounts
WHERE account_id = 101;

UPDATE accounts
SET balance = balance - 500
WHERE account_id = 101;

COMMIT;


-- ============================================================
-- TRANSACTION DECISION GUIDE
-- ============================================================

-- COMMIT
--   Persist all successful operations.

-- ROLLBACK
--   Undo all operations since BEGIN.

-- SAVEPOINT
--   Create a partial rollback point.

-- SELECT ... FOR UPDATE
--   Lock selected rows for modification within a transaction.

-- SERIALIZABLE
--   Provide the strongest standard isolation guarantee,
--   potentially at the cost of reduced concurrency.

-- Practical rule:
--
-- If multiple operations together represent one business action,
-- they should generally belong to the same transaction boundary.