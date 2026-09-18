-- Day 49 — Production SQL Troubleshooting
-- PostgreSQL-oriented diagnostic queries.
--
-- These queries are read-only examples intended for an incident investigation.
-- Run them with an appropriately restricted operational role.

-- 1. Identify active sessions and long-running statements.
SELECT
    pid,
    usename,
    state,
    now() - query_start AS query_age,
    wait_event_type,
    wait_event,
    LEFT(query, 200) AS query_preview
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY query_age DESC;

-- 2. Find statements with high cumulative execution time.
SELECT
    queryid,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_exec_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_exec_ms,
    rows,
    LEFT(query, 200) AS query_preview
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 3. Inspect currently waiting sessions.
SELECT
    pid,
    usename,
    wait_event_type,
    wait_event,
    state,
    LEFT(query, 200) AS query_preview
FROM pg_stat_activity
WHERE wait_event IS NOT NULL
ORDER BY pid;

-- 4. Find sessions blocked by another PostgreSQL backend.
SELECT
    blocked.pid AS blocked_pid,
    blocker.pid AS blocker_pid,
    blocked.query AS blocked_query,
    blocker.query AS blocker_query
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocker
    ON blocker.pid = ANY(pg_blocking_pids(blocked.pid));

-- 5. Check transaction age that can indicate operational risk.
SELECT
    pid,
    usename,
    now() - xact_start AS transaction_age,
    state,
    LEFT(query, 200) AS query_preview
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start;

-- 6. Troubleshooting workflow:
--    a) Confirm the symptom and affected time window.
--    b) Check active sessions and wait events.
--    c) Inspect expensive statements and lock blockers.
--    d) Compare current behavior with the deployment change window.
--    e) Mitigate safely before attempting a permanent fix.
