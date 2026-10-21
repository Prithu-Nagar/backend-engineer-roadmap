-- Day 82: PostgreSQL transaction and query-optimization review.
-- Schema assumptions are illustrative; adapt table/column names before running.

-- 1. Review isolation anomalies and keep the read/validate/write sequence
-- inside one transaction. SELECT ... FOR UPDATE is one option when a row
-- already exists and must be serialized.
BEGIN;
SELECT account_id, balance
FROM accounts
WHERE account_id = :account_id
FOR UPDATE;

-- Application validates sufficient balance before issuing the update.
-- UPDATE accounts SET balance = balance - :amount
-- WHERE account_id = :account_id AND balance >= :amount;
-- Check affected-row count; roll back if the debit was not applied.
COMMIT;

-- 2. Prefer an atomic conditional update for inventory reservation.
-- The affected-row count indicates whether stock was available.
UPDATE inventory
SET available_quantity = available_quantity - :quantity
WHERE product_id = :product_id
  AND :quantity > 0
  AND available_quantity >= :quantity;

-- 3. Detect duplicate idempotency keys before repeating a write.
-- A UNIQUE constraint on (client_id, idempotency_key) is required for
-- concurrency safety; application-level SELECT alone is not sufficient.
SELECT client_id, idempotency_key, request_status, response_payload
FROM idempotency_records
WHERE client_id = :client_id
  AND idempotency_key = :idempotency_key;

-- 4. Query-optimization review: inspect predicates, row counts, and sort cost.
SELECT customer_id, COUNT(*) AS completed_orders, SUM(total_amount) AS spend
FROM orders
WHERE status = 'completed'
  AND created_at >= :start_timestamp
  AND created_at < :end_timestamp
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY spend DESC
LIMIT 50;

-- Candidate index to evaluate (not blindly apply):
-- CREATE INDEX CONCURRENTLY idx_orders_status_created_customer
--     ON orders (status, created_at, customer_id)
--     INCLUDE (total_amount);
-- Compare EXPLAIN (ANALYZE, BUFFERS) on representative data, and consider
-- write amplification, storage, selectivity, and existing indexes.

-- Interview checklist:
-- * Explain atomicity, consistency, isolation, and durability.
-- * Distinguish lost updates, non-repeatable reads, and write skew.
-- * Keep transactions short; use a consistent lock order to reduce deadlocks.
-- * Retry serialization failures/deadlocks only with bounded attempts.
-- * Never claim an index helps until the execution plan and workload support it.
