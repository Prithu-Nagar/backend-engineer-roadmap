-- Day 46 — Query Monitoring
--
-- Production query monitoring should identify expensive, slow, frequent, and
-- resource-heavy statements without exposing sensitive application data.

-- 1. Statements consuming the most total execution time.
SELECT
    query,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_exec_time_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_time_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 2. Statements with the highest average latency.
SELECT
    query,
    calls,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_time_ms,
    rows
FROM pg_stat_statements
WHERE calls > 0
ORDER BY mean_exec_time DESC
LIMIT 20;

-- 3. High-frequency statements. A fast query can still matter when executed
-- thousands of times per minute.
SELECT
    query,
    calls,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_time_ms
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 20;

-- 4. Statements returning many rows per call, which can signal inefficient
-- filtering, missing pagination, or an overly broad result set.
SELECT
    query,
    calls,
    rows,
    ROUND(rows::numeric / NULLIF(calls, 0), 2) AS rows_per_call
FROM pg_stat_statements
WHERE calls > 0
ORDER BY rows_per_call DESC
LIMIT 20;

-- 5. PostgreSQL logging controls commonly used with query monitoring.
-- Configure through the database configuration mechanism rather than relying
-- on application SQL for permanent server settings.
--
-- log_min_duration_statement = 500
-- log_statement = 'none'
-- log_lock_waits = on
-- deadlock_timeout = '1s'

-- 6. Reset statistics only after capturing the current observation window.
-- SELECT pg_stat_statements_reset();

-- Monitoring guidance:
-- * Track latency percentiles when the monitoring platform supports them.
-- * Alert on sustained regressions rather than one isolated slow query.
-- * Correlate query timing with application request IDs and timestamps.
-- * Never log passwords, tokens, or other sensitive request values.
