-- Day 37 — Database Observability & Slow Query Logs
--
-- PostgreSQL provides runtime statistics through pg_stat_statements and
-- server logging controls. Observability should help identify slow queries,
-- high-frequency queries, failures, and resource-heavy workloads.

-- Enable the extension once at the database level.
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top statements by total execution time.
SELECT
    query,
    calls,
    total_exec_time,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_time,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Statements with the highest average latency.
SELECT
    query,
    calls,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_time,
    rows
FROM pg_stat_statements
WHERE calls > 0
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Statements that process many rows relative to their execution count.
SELECT
    query,
    calls,
    rows,
    ROUND(rows::numeric / NULLIF(calls, 0), 2) AS rows_per_call,
    mean_exec_time
FROM pg_stat_statements
WHERE calls > 0
ORDER BY rows_per_call DESC
LIMIT 20;

-- Useful PostgreSQL logging settings for slow-query investigation.
-- These are configuration examples; apply them through PostgreSQL's supported
-- configuration mechanisms rather than as ordinary application SQL.
--
-- log_min_duration_statement = 500
-- log_min_duration_sample = 100
-- log_statement = 'none'
--
-- A duration of 500 ms means completed statements taking at least 500 ms are
-- written to the server log. Sampling can reduce log volume on busy systems.

-- Reset collected statement statistics after an intentional observation window.
-- Use carefully because this clears the accumulated pg_stat_statements data.
-- SELECT pg_stat_statements_reset();

-- Correlate a slow application request with the database statement by keeping
-- request/correlation IDs in application logs and timestamps in both systems.
-- The database view alone cannot reconstruct an end-to-end distributed trace.
