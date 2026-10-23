-- Day 84 — Production database review
-- PostgreSQL examples: verify names and constraints against the real schema.

-- 1. Check connection capacity and current sessions before changing pool sizes.
SELECT state, COUNT(*) AS connection_count
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY state
ORDER BY state;

-- 2. Inspect database/table size before capacity planning.
SELECT
    schemaname,
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(
        format('%I.%I', schemaname, relname)::regclass
    )) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(
    format('%I.%I', schemaname, relname)::regclass
) DESC
LIMIT 20;

-- 3. Use a transaction and a conditional update for a concurrency-safe change.
BEGIN;
UPDATE tasks
SET status = 'in_progress',
    updated_at = CURRENT_TIMESTAMP
WHERE task_id = '00000000-0000-0000-0000-000000000001'
  AND status = 'todo';
-- Application should verify the affected-row count before COMMIT.
COMMIT;

-- 4. Confirm constraints and indexes exist; avoid duplicate index creation.
SELECT conname, contype
FROM pg_constraint
WHERE conrelid = 'tasks'::regclass
ORDER BY conname;

SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'tasks'
ORDER BY indexname;

-- 5. Production review checklist:
-- - Credentials are supplied through a secret manager/environment, not source.
-- - Application role has least-privilege grants.
-- - Connection pool limits fit database capacity and worker counts.
-- - Migrations are reviewed, repeatable, and have a rollback/recovery plan.
-- - Backups have tested restore procedures and explicit RPO/RTO targets.
-- - Slow-query monitoring and representative EXPLAIN plans are reviewed.
-- - Retry behavior is bounded; transaction retries are safe and idempotent.
-- - Destructive changes and EXPLAIN ANALYZE are run only with appropriate safeguards.
