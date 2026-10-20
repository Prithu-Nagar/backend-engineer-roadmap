-- Day 81 — Full SQL interview set (PostgreSQL).
-- Assumed tables: customers(customer_id, name, created_at), orders(order_id,
-- customer_id, order_date, status, total_amount), order_items(order_id,
-- product_id, quantity, unit_price). Verify names and types against your schema.

-- 1. Customers with total completed-order revenue, including customers with none.
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.total_amount), 0) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY completed_revenue DESC, c.customer_id;

-- 2. Rank customers by completed revenue; ties share the same rank.
WITH customer_revenue AS (
    SELECT c.customer_id, c.name,
           COALESCE(SUM(o.total_amount), 0) AS revenue
    FROM customers AS c
    LEFT JOIN orders AS o
      ON o.customer_id = c.customer_id AND o.status = 'completed'
    GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, revenue,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM customer_revenue
ORDER BY revenue_rank, customer_id;

-- 3. Monthly completed-order totals and month-over-month change.
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)::date
)
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change_from_previous_month
FROM monthly
ORDER BY month;

-- 4. Find products with at least 100 units sold. Assumes product_id is available
-- in order_items; join a products table if product names are needed.
SELECT product_id, SUM(quantity) AS units_sold,
       SUM(quantity * unit_price) AS gross_sales
FROM order_items
GROUP BY product_id
HAVING SUM(quantity) >= 100
ORDER BY units_sold DESC, product_id;

-- 5. Interview discussion: consider (status, order_date) for queries filtering by
-- status and date. Validate with EXPLAIN (ANALYZE, BUFFERS) on representative data;
-- do not add an index without measuring read benefit and write/storage cost.
-- EXPLAIN (ANALYZE, BUFFERS)
-- SELECT order_id, customer_id, total_amount FROM orders
-- WHERE status = 'completed' AND order_date >= DATE '2026-01-01';
