-- Day 39 — Database Design Review
-- PostgreSQL-oriented review for the Expense Tracker schema.
--
-- The examples review primary keys, constraints, indexes, access patterns,
-- and transaction boundaries rather than introducing a new schema feature.

CREATE TABLE IF NOT EXISTS expenses_review (
    id BIGSERIAL PRIMARY KEY,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    expense_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Match indexes to the queries the application actually runs.
CREATE INDEX IF NOT EXISTS idx_expenses_review_category_date
    ON expenses_review (category, expense_date DESC);

CREATE INDEX IF NOT EXISTS idx_expenses_review_date
    ON expenses_review (expense_date DESC);

-- A common review query: filter by category and a bounded date range.
SELECT id, amount, category, expense_date
FROM expenses_review
WHERE category = 'travel'
  AND expense_date >= DATE '2026-09-01'
  AND expense_date < DATE '2026-10-01'
ORDER BY expense_date DESC, id DESC
LIMIT 20;

-- Inspect the query plan before adding an index or changing the schema.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, amount, category, expense_date
FROM expenses_review
WHERE category = 'travel'
  AND expense_date >= DATE '2026-09-01'
  AND expense_date < DATE '2026-10-01'
ORDER BY expense_date DESC, id DESC
LIMIT 20;

-- Keep multi-step business changes inside one transaction.
BEGIN;

UPDATE expenses_review
SET amount = 2750.00,
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- COMMIT only after all required statements for the unit of work succeed.
COMMIT;

-- Design review checklist:
-- * Every table has a stable primary key.
-- * Domain invariants are enforced with NOT NULL/CHECK/UNIQUE constraints.
-- * Indexes support measured access patterns rather than every column.
-- * Composite index column order follows filtering and ordering needs.
-- * Queries are reviewed with EXPLAIN (ANALYZE, BUFFERS).
-- * Transactions are kept short and owned by the application boundary.
-- * Schema changes remain backward compatible during rolling deployments.
