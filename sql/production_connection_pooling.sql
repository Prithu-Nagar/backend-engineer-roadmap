-- Day 45 — Connection Pooling and Production Database Settings
--
-- This file records production-oriented PostgreSQL checks. Pool sizing is
-- normally enforced by the application or a pooler rather than by opening a
-- database connection for every request.

-- Inspect the server-side connection ceiling.
SELECT name, setting
FROM pg_settings
WHERE name IN ('max_connections', 'shared_buffers');

-- Inspect active connections by database.
SELECT datname, count(*) AS connection_count
FROM pg_stat_activity
WHERE datname IS NOT NULL
GROUP BY datname
ORDER BY connection_count DESC;

-- Production checklist:
-- 1. Use a bounded application connection pool.
-- 2. Keep pool size below the database connection budget.
-- 3. Reserve capacity for administrative and migration connections.
-- 4. Set connection and statement timeouts appropriate to the workload.
-- 5. Monitor pool saturation, wait time, and database connections.
-- 6. Keep credentials and DATABASE_URL outside source control.
-- 7. Validate settings separately for development, staging, and production.
