-- Day 83 — Indexing and schema review
-- PostgreSQL examples; adapt table and column names to the capstone schema.

-- 1. Model access patterns before adding indexes.
-- Typical request: fetch a user's active tasks, newest first.
CREATE INDEX IF NOT EXISTS idx_tasks_owner_status_created
    ON tasks (owner_id, status, created_at DESC);

-- 2. Partial index for a frequently queried subset.
CREATE INDEX IF NOT EXISTS idx_tasks_open_due_at
    ON tasks (due_at)
    WHERE status IN ('todo', 'in_progress');

-- 3. Enforce business invariants with database constraints.
-- Use a unique constraint when duplicates are invalid, not just an
-- application-level pre-check that can race under concurrent requests.
ALTER TABLE tasks
    ADD CONSTRAINT tasks_priority_range
    CHECK (priority BETWEEN 1 AND 5);

-- 4. Inspect plans using representative parameters and realistic data.
EXPLAIN (ANALYZE, BUFFERS)
SELECT task_id, title, status, created_at
FROM tasks
WHERE owner_id = '00000000-0000-0000-0000-000000000001'
  AND status = 'todo'
ORDER BY created_at DESC
LIMIT 50;

-- 5. Review existing indexes before adding duplicates.
SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 6. Example schema review checklist:
-- - Primary keys uniquely identify rows.
-- - Foreign keys protect referential integrity.
-- - NOT NULL / CHECK / UNIQUE constraints encode valid states.
-- - Composite index order matches equality filters, range filters,
--   and ordering requirements.
-- - Write overhead and index storage are considered.
-- - EXPLAIN ANALYZE is run only in a safe environment because it executes
--   the statement; use plain EXPLAIN when execution is not appropriate.
