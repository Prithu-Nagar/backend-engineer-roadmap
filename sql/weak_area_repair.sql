-- Day 80 — SQL weak-area repair
-- Dialect: PostgreSQL.
-- Assumed schema:
-- customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)
--
-- Use the query matching the weakest Day 79 result. Explain NULL handling,
-- join cardinality, ordering, and index trade-offs before checking the query.

-- 1. Include customers with no completed orders.
SELECT
    c.customer_id,
    c.name,
    COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
    ON o.customer_id = c.customer_id
   AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Latest two orders per customer, with deterministic tie-breaking.
WITH ranked_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        o.total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC, o.order_id DESC
        ) AS row_num
    FROM orders AS o
)
SELECT order_id, customer_id, order_date, status, total_amount
FROM ranked_orders
WHERE row_num <= 2
ORDER BY customer_id, row_num;

-- 3. Product revenue, including products that have never been ordered.
SELECT
    p.product_id,
    p.product_name,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
FROM products AS p
LEFT JOIN order_items AS oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC, p.product_id;

-- 4. Weak-area review: inspect the plan with representative production-like data.
-- EXPLAIN (ANALYZE, BUFFERS)
-- SELECT order_id, order_date, total_amount
-- FROM orders
-- WHERE customer_id = 42 AND status = 'completed'
-- ORDER BY order_date DESC
-- LIMIT 20;
--
-- Evaluate (customer_id, status, order_date DESC) as a candidate index only
-- after checking existing indexes, selectivity, and write overhead.
