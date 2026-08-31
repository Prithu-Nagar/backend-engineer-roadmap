-- Day 31 — SQL Transaction Isolation Levels
--
-- PostgreSQL-oriented examples for understanding:
-- - READ COMMITTED
-- - REPEATABLE READ
-- - SERIALIZABLE
-- - Dirty reads
-- - Non-repeatable reads
-- - Phantom reads
--
-- Run concurrent examples in separate database sessions.

-- ============================================================
-- ISOLATION LEVELS
-- ============================================================

-- PostgreSQL supports:
-- READ UNCOMMITTED (behaves like READ COMMITTED in PostgreSQL)
-- READ COMMITTED
-- REPEATABLE READ
-- SERIALIZABLE

-- READ COMMITTED
-- Each statement sees data committed before that statement began.

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT *
FROM accounts
WHERE account_id = 1;

COMMIT;

-- REPEATABLE READ
-- Statements in the same transaction use a consistent snapshot.

BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT *
FROM accounts
WHERE account_id = 1;

-- Perform additional reads in this transaction.

COMMIT;

-- SERIALIZABLE
-- Provides the strongest isolation and may require a transaction
-- to be retried when concurrent work cannot be serialized safely.

BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT *
FROM accounts
WHERE account_id = 1;

COMMIT;

-- ============================================================
-- DIRTY READ
-- ============================================================

-- A dirty read occurs when one transaction reads another
-- transaction's uncommitted change.
--
-- PostgreSQL does not expose dirty reads because READ UNCOMMITTED
-- behaves as READ COMMITTED.

-- Session A:
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 1;

-- Do not commit yet.

-- Session B:
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT balance
FROM accounts
WHERE account_id = 1;

-- Session B does not see Session A's uncommitted update.

ROLLBACK;

-- Session A:
ROLLBACK;

-- ============================================================
-- NON-REPEATABLE READ
-- ============================================================

-- A non-repeatable read occurs when the same row is read twice
-- and another committed transaction changes it between reads.
--
-- READ COMMITTED permits this pattern.

-- Session A:
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT balance
FROM accounts
WHERE account_id = 1;

-- Session B commits an UPDATE to account_id = 1 here.

-- Session A:
SELECT balance
FROM accounts
WHERE account_id = 1;

COMMIT;

-- Under REPEATABLE READ, Session A keeps the same snapshot for
-- the transaction, so the second read does not see the later commit.

-- ============================================================
-- PHANTOM READ
-- ============================================================

-- A phantom read occurs when a repeated query over a set of rows
-- observes a different set because another transaction inserted,
-- deleted, or changed matching rows.
--
-- PostgreSQL's REPEATABLE READ uses a transaction snapshot, while
-- SERIALIZABLE adds stronger protection against conflicting
-- concurrent transactions.

-- Session A:
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT COUNT(*)
FROM expenses
WHERE amount >= 1000;

-- Session B commits a new matching expense here.

-- Session A:
SELECT COUNT(*)
FROM expenses
WHERE amount >= 1000;

COMMIT;

-- ============================================================
-- PRACTICAL GUIDELINES
-- ============================================================

-- Use READ COMMITTED when normal request-level consistency is enough.
-- Use REPEATABLE READ when a transaction needs a stable snapshot.
-- Use SERIALIZABLE when correctness requires the strongest
-- transaction isolation and the application can retry serialization
-- failures.
--
-- Keep transactions short and lock only the rows that must be protected.
