-- ============================================================
-- Day 42 — Database Migrations in Containers
-- ============================================================
--
-- This is a standalone Day 42 learning example, not part of the current
-- Task Manager Compose startup. The example assumes an Expense Tracker
-- `expenses` table exists before its index migration runs.
--
-- In a production environment, a dedicated migration tool should
-- own migration ordering and execution history. This example keeps
-- the migration boundary explicit for local container practice.
-- ============================================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Migration 001: add a useful lookup index to the Expense Tracker.
CREATE INDEX IF NOT EXISTS idx_expenses_category
    ON expenses (category);

INSERT INTO schema_migrations (version)
VALUES ('001_expense_category_index')
ON CONFLICT (version) DO NOTHING;
