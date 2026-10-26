-- Day 87 — Full timed SQL assessment
-- Dialect: PostgreSQL. Suggested time: 45 minutes.
-- Assumed schema:
-- customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)

-- 1. Include every customer and their completed-order revenue.
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
 AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Rank each customer's orders from newest to oldest.
SELECT order_id, customer_id, order_date, status,
       ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY order_date DESC, order_id DESC
       ) AS order_rank
FROM orders;

-- 3. Find products whose revenue is above the average product revenue.
WITH product_revenue AS (
    SELECT p.product_id, p.product_name,
           COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
    FROM products AS p
    LEFT JOIN order_items AS oi ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT product_id, product_name, revenue
FROM product_revenue
WHERE revenue > (SELECT AVG(revenue) FROM product_revenue)
ORDER BY revenue DESC;

-- 4. Find customers with at least two completed orders.
SELECT customer_id, COUNT(*) AS completed_order_count
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY completed_order_count DESC, customer_id;

-- 5. Explain and compare this query with and without a suitable index.
-- EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 42 AND status = 'completed'
ORDER BY order_date DESC
LIMIT 20;

-- Before creating indexes, inspect existing indexes and representative plans.
-- Candidate only; validate workload and write overhead first:
-- CREATE INDEX CONCURRENTLY idx_orders_customer_status_date
--     ON orders (customer_id, status, order_date DESC);

-- Assessment checklist:
-- - Explain LEFT JOIN filter placement and NULL handling.
-- - Distinguish WHERE from HAVING and ROW_NUMBER from RANK.
-- - Discuss transaction boundaries, isolation, and integrity constraints.
-- - Avoid claiming a query is faster without measuring representative plans.
