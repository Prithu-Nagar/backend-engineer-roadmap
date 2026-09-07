-- Day 38 — Data Integrity Under Concurrent Writes
-- PostgreSQL examples.
--
-- The examples show three complementary techniques:
-- 1. Unique constraints for duplicate-write protection.
-- 2. Row locks for coordinated read/modify/write operations.
-- 3. Optimistic version checks when waiting on a lock is undesirable.

CREATE TABLE IF NOT EXISTS expense_requests (
    id BIGSERIAL PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Concurrent requests with the same idempotency key cannot create two rows.
INSERT INTO expense_requests (idempotency_key, amount)
VALUES ('req-1001', 2500.00)
ON CONFLICT (idempotency_key) DO NOTHING;

-- Row locking protects a read/modify/write operation on one logical row.
CREATE TABLE IF NOT EXISTS account_balances (
    account_id BIGINT PRIMARY KEY,
    balance NUMERIC(14, 2) NOT NULL CHECK (balance >= 0)
);

BEGIN;

SELECT account_id, balance
FROM account_balances
WHERE account_id = 1
FOR UPDATE;

UPDATE account_balances
SET balance = balance - 100.00
WHERE account_id = 1
  AND balance >= 100.00;

COMMIT;

-- Optimistic concurrency uses a version column instead of holding a lock.
CREATE TABLE IF NOT EXISTS expense_items (
    expense_id BIGSERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    version INTEGER NOT NULL DEFAULT 1
);

-- The application first reads the current version.
-- The update succeeds only if nobody changed the row in the meantime.
UPDATE expense_items
SET amount = 2750.00,
    version = version + 1
WHERE expense_id = 1
  AND version = 3;

-- If row_count = 0, the caller should reload the row and resolve the conflict
-- rather than silently overwriting another transaction's update.

-- For critical multi-row invariants, SERIALIZABLE can provide stronger
-- guarantees. Serialization failures must be retried by the application.
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

UPDATE account_balances
SET balance = balance - 50.00
WHERE account_id = 1
  AND balance >= 50.00;

COMMIT;

-- Production guidance:
-- * Keep transactions short.
-- * Lock rows in a consistent order when multiple rows are required.
-- * Prefer atomic SQL conditions for simple invariants.
-- * Treat unique-constraint and serialization failures as expected concurrency
--   outcomes that the application must handle explicitly.
