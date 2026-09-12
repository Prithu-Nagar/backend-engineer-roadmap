-- Day 43 — Production Schema Migration Practices
--
-- Goals:
--   1. Track applied migrations.
--   2. Make additive changes safe to rerun.
--   3. Keep schema changes explicit and auditable.
--   4. Use a transaction for an atomic migration where supported.

BEGIN;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(64) PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Example additive migration: create an index only when it does not exist.
CREATE INDEX IF NOT EXISTS idx_expenses_category_created_at
    ON expenses (category_id, created_at DESC);

INSERT INTO schema_migrations (version)
VALUES ('2026_09_12_add_expense_category_created_index')
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- Production migration checklist:
-- * Prefer backward-compatible changes first (expand), then cleanup (contract).
-- * Avoid destructive changes in the same release that starts using the new schema.
-- * Keep migrations small, ordered, reviewable, and reversible where practical.
-- * Test migrations against a production-like database before deployment.
-- * Monitor lock duration and table size for large schema changes.
