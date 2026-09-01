-- Day 32 — Deadlocks, Detection and Avoidance
--
-- PostgreSQL-oriented examples. Run the two-session examples in separate
-- database sessions to observe lock interactions.

-- ============================================================
-- DEADLOCK SHAPE
-- ============================================================

-- Session A:
BEGIN;
UPDATE accounts
SET balance = balance - 10
WHERE account_id = 1;

-- Session B, before Session A commits:
BEGIN;
UPDATE accounts
SET balance = balance - 20
WHERE account_id = 2;

-- Session A now requests the row held by Session B:
UPDATE accounts
SET balance = balance + 10
WHERE account_id = 2;

-- Session B now requests the row held by Session A:
UPDATE accounts
SET balance = balance + 20
WHERE account_id = 1;

-- PostgreSQL detects the cycle and aborts one transaction.
-- The application should handle the error and retry when appropriate.

ROLLBACK;

-- ============================================================
-- CONSISTENT LOCK ORDER
-- ============================================================

-- A common avoidance strategy is to acquire multiple locks in the same
-- deterministic order in every transaction.

BEGIN;

UPDATE accounts
SET balance = balance - 10
WHERE account_id = 1;

UPDATE accounts
SET balance = balance + 10
WHERE account_id = 2;

COMMIT;

-- Another transaction performing the same transfer pattern should also
-- lock account_id 1 before account_id 2.

-- ============================================================
-- DETECTION / OBSERVABILITY
-- ============================================================

-- Inspect active sessions and wait states:
SELECT
    pid,
    application_name,
    state,
    wait_event_type,
    wait_event,
    query
FROM pg_stat_activity
WHERE state <> 'idle';

-- Inspect granted and waiting locks:
SELECT
    locktype,
    relation::regclass AS relation_name,
    pid,
    mode,
    granted
FROM pg_locks
WHERE relation IS NOT NULL;

-- PostgreSQL logs can also record deadlock details when log settings are
-- configured appropriately.

-- ============================================================
-- AVOIDANCE CHECKLIST
-- ============================================================

-- 1. Acquire locks in a consistent order.
-- 2. Keep transactions short.
-- 3. Avoid unnecessary database work while holding locks.
-- 4. Use appropriate lock modes rather than stronger locks by default.
-- 5. Set sensible lock/statement timeouts.
-- 6. Treat deadlock failures as retryable when the operation is safe to retry.
-- 7. Make retries bounded and observable.
