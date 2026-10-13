-- Day 74 — SQL Interview Set 4: Indexes and Query Optimization
-- Dialect: PostgreSQL-oriented SQL. Adapt EXPLAIN options to your database.
-- Assumed tables:
--   users(id, email, created_at, status)
--   orders(id, user_id, status, created_at, total_amount)
--   order_items(id, order_id, product_id, quantity, unit_price)

-- 1. Find recent orders for one user. Explain which index could support this
--    filter and ordering pattern.
SELECT id, status, created_at, total_amount
FROM orders
WHERE user_id = 42
ORDER BY created_at DESC
LIMIT 20;

-- Candidate index for the query above. Validate with workload and query plans
-- before creating it in a production migration.
CREATE INDEX IF NOT EXISTS idx_orders_user_created_at
    ON orders (user_id, created_at DESC);

-- 2. Compare a single-column index with a composite index for queries filtering
--    by user_id and status. Column order should follow common predicates and
--    sort requirements, not a universal rule.
CREATE INDEX IF NOT EXISTS idx_orders_user_status_created_at
    ON orders (user_id, status, created_at DESC);

SELECT id, created_at, total_amount
FROM orders
WHERE user_id = 42
  AND status = 'completed'
ORDER BY created_at DESC
LIMIT 20;

-- 3. Inspect the query plan. EXPLAIN ANALYZE executes the query; use care with
--    statements that mutate data or have expensive side effects.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, user_id, created_at
FROM orders
WHERE created_at >= TIMESTAMP '2026-01-01 00:00:00'
  AND created_at < TIMESTAMP '2026-02-01 00:00:00';

-- 4. Rewrite a non-sargable date predicate to a range predicate so an index on
--    created_at can potentially be used.
-- Avoid: WHERE DATE(created_at) = DATE '2026-01-15'
SELECT id, created_at
FROM orders
WHERE created_at >= TIMESTAMP '2026-01-15 00:00:00'
  AND created_at < TIMESTAMP '2026-01-16 00:00:00';

-- 5. Identify users with at least five completed orders. Compare aggregation
--    cost with the number of rows scanned and consider a partial index only
--    if the predicate is selective and supported by the workload.
SELECT user_id, COUNT(*) AS completed_order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id
HAVING COUNT(*) >= 5;

-- PostgreSQL option to evaluate for a stable, frequent predicate:
CREATE INDEX IF NOT EXISTS idx_orders_completed_user
    ON orders (user_id)
    WHERE status = 'completed';

-- 6. Find users whose email is duplicated. A unique constraint/index is the
--    correct long-term prevention mechanism if the business rule requires it.
SELECT email, COUNT(*) AS duplicate_count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- 7. Interview discussion prompts:
--    * When can an index make writes slower?
--    * What is the difference between estimated and actual row counts?
--    * What do sequential scans, index scans, and bitmap scans indicate?
--    * Why might the optimizer ignore an available index?
--    * How do selectivity, statistics, table size, and cache state affect plans?
--    * Why should a production index be created through a migration?
--    * What is the risk of adding every suggested index?
