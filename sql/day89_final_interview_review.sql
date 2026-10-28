-- Day 89 — Final SQL interview review
-- Dialect: PostgreSQL.
-- Assumed schema: customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)

-- 1. Aggregate completed revenue while retaining customers with no matches.
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
 AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Return the latest order per customer with deterministic tie-breaking.
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

-- 3. Compare each product's revenue with its category average, including zeroes.
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

-- 4. Transaction review drill: explain isolation, constraints, and rollback.
-- BEGIN;
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- COMMIT; -- ROLLBACK if any validation or update fails.

-- 5. Inspect representative query plans before proposing an index.
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 42 AND status = 'completed'
ORDER BY order_date DESC, order_id DESC
LIMIT 20;

-- Interview checklist:
-- * Explain WHERE vs HAVING and INNER vs LEFT JOIN.
-- * Explain ROW_NUMBER vs RANK vs DENSE_RANK.
-- * Describe composite-index column order and write overhead.
-- * Distinguish atomicity, isolation levels, and integrity constraints.
-- * Use actual plan evidence; do not assume an index is beneficial.
