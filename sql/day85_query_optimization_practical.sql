-- Day 85 — Query optimization practical
-- PostgreSQL examples. Confirm table/column names and test plans on representative data.

-- 1. Establish a baseline using a realistic, selective query.
EXPLAIN (ANALYZE, BUFFERS)
SELECT task_id, title, status, updated_at
FROM tasks
WHERE user_id = 42
  AND status = 'open'
ORDER BY updated_at DESC
LIMIT 50;

-- 2. A composite index may support the filter and ordering above.
-- Validate write overhead and index usefulness before retaining it.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_user_status_updated
ON tasks (user_id, status, updated_at DESC);

-- 3. Compare the plan after index creation. Do not assume an index is always faster.
EXPLAIN (ANALYZE, BUFFERS)
SELECT task_id, title, status, updated_at
FROM tasks
WHERE user_id = 42
  AND status = 'open'
ORDER BY updated_at DESC
LIMIT 50;

-- 4. Keyset pagination avoids scanning increasingly large OFFSET ranges.
-- The cursor values should come from the final row of the previous page.
SELECT task_id, title, updated_at
FROM tasks
WHERE user_id = 42
  AND (updated_at, task_id) < (TIMESTAMP '2026-10-24 08:00:00', 9000)
ORDER BY updated_at DESC, task_id DESC
LIMIT 50;

-- 5. Inspect table statistics and index usage after representative workload.
ANALYZE tasks;
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'tasks'
ORDER BY idx_scan DESC;

-- Review checklist:
-- - Compare estimated rows with actual rows and investigate large differences.
-- - Review shared/local buffer reads, sort operations, and join strategies.
-- - Test with realistic parameter values and data volume.
-- - Avoid running EXPLAIN ANALYZE on expensive or mutating statements without safeguards.
-- - Account for index storage, write amplification, and maintenance cost.
