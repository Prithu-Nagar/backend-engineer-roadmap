-- Day 79 — Mixed SQL timed assessment
-- Dialect: PostgreSQL. Suggested time: 35 minutes.
-- Schema assumptions:
-- customers(customer_id, name, created_at)
-- orders(order_id, customer_id, order_date, status, total_amount)
-- order_items(order_id, product_id, quantity, unit_price)
-- products(product_id, product_name, category)

-- 1. Find each customer's total completed-order revenue, including customers
--    who have never placed a completed order.
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

-- 2. Return the three most recent orders per customer.
WITH ranked_orders AS (
    SELECT
        o.*,
        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC, o.order_id DESC
        ) AS order_rank
    FROM orders AS o
)
SELECT order_id, customer_id, order_date, status, total_amount
FROM ranked_orders
WHERE order_rank <= 3
ORDER BY customer_id, order_rank;

-- 3. Find products whose revenue exceeds the average product revenue.
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
    FROM products AS p
    LEFT JOIN order_items AS oi ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT product_id, product_name, revenue
FROM product_revenue
WHERE revenue > (SELECT AVG(revenue) FROM product_revenue)
ORDER BY revenue DESC;

-- 4. Identify customers with at least two completed orders.
SELECT customer_id, COUNT(*) AS completed_order_count
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY completed_order_count DESC, customer_id;

-- 5. Review plan and index candidates before adding indexes in production:
-- EXPLAIN (ANALYZE, BUFFERS)
-- SELECT order_id, order_date, total_amount
-- FROM orders
-- WHERE customer_id = 42 AND status = 'completed'
-- ORDER BY order_date DESC
-- LIMIT 20;
--
-- Possible index to evaluate against actual workload:
-- CREATE INDEX CONCURRENTLY idx_orders_customer_status_date
--     ON orders (customer_id, status, order_date DESC);
-- Do not create indexes blindly: compare query plans, write overhead, and
-- existing indexes first.
