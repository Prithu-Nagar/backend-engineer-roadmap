-- Day 88 — SQL weak-area repair
-- Dialect: PostgreSQL.
-- Assumed schema: customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)

-- 1. Keep customers with no completed orders and return zero revenue.
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
 AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Rank orders within each customer. Include a deterministic tie-breaker.
SELECT order_id, customer_id, order_date,
       ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY order_date DESC, order_id DESC
       ) AS newest_first
FROM orders;

-- 3. Find products with revenue above the average across all products,
-- including products with zero revenue in the average.
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
ORDER BY revenue DESC, product_id;

-- 4. Compare estimated and actual plans on representative data.
-- EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 42
  AND status = 'completed'
ORDER BY order_date DESC, order_id DESC
LIMIT 20;

-- Candidate index only: validate selectivity, read benefit, and write cost.
-- CREATE INDEX CONCURRENTLY idx_orders_customer_status_date
--     ON orders (customer_id, status, order_date DESC, order_id DESC);

-- Repair checklist:
-- * Explain why the status predicate belongs in JOIN for query 1.
-- * Distinguish WHERE, HAVING, ROW_NUMBER, RANK, and DENSE_RANK.
-- * Check transaction boundaries, constraints, and isolation assumptions.
-- * Never infer performance from index existence alone; inspect actual plans.
