-- Day 90 — Final SQL assessment and long-term practice plan
-- Dialect: PostgreSQL.
-- Assumed schema: customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)

-- 1. Retain every customer while calculating completed-order revenue.
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
 AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Find the latest order per customer with deterministic tie-breaking.
WITH ranked_orders AS (
    SELECT o.*,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY order_date DESC, order_id DESC
           ) AS row_num
    FROM orders AS o
)
SELECT order_id, customer_id, order_date, total_amount
FROM ranked_orders
WHERE row_num = 1;

-- 3. Compare each product's revenue with its category average.
WITH product_revenue AS (
    SELECT p.product_id, p.product_name, p.category,
           COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
    FROM products AS p
    LEFT JOIN order_items AS oi ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT product_id, product_name, category, revenue,
       AVG(revenue) OVER (PARTITION BY category) AS category_average
FROM product_revenue
ORDER BY category, revenue DESC, product_id;

-- 4. Transaction drill: execute both updates atomically in a real test database.
-- BEGIN;
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- COMMIT; -- ROLLBACK if validation or either update fails.

-- 5. Inspect real query plans before proposing an index.
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 42 AND status = 'completed'
ORDER BY order_date DESC, order_id DESC
LIMIT 20;

-- Final checklist:
-- * Explain joins, filtering, grouping, and window functions.
-- * Explain transaction boundaries, isolation, and integrity constraints.
-- * Compare indexes using measured plans and write overhead.
-- * Parameterize application queries; never concatenate untrusted input.
-- * Record dialect and schema assumptions when sharing a solution.
