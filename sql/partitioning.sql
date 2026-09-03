-- Day 34 — PostgreSQL Partitioning Concepts
--
-- Partitioning keeps one logical table while storing rows in smaller child
-- tables. RANGE partitioning is useful for time-based data such as expenses,
-- events, and audit records.

CREATE TABLE expense_events (
    id BIGINT NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    PRIMARY KEY (id, expense_date)
) PARTITION BY RANGE (expense_date);

CREATE TABLE expense_events_2026_09
    PARTITION OF expense_events
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');

CREATE TABLE expense_events_2026_10
    PARTITION OF expense_events
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

-- The query can target the logical parent. PostgreSQL can prune partitions
-- that cannot contain rows matching the date predicate.
EXPLAIN
SELECT category, SUM(amount)
FROM expense_events
WHERE expense_date >= DATE '2026-09-01'
  AND expense_date < DATE '2026-10-01'
GROUP BY category;

-- Partition-local indexes can support common access patterns.
CREATE INDEX idx_expense_events_sep_category
    ON expense_events_2026_09 (category, expense_date);

-- A default partition can catch rows that do not match a declared range.
-- It should be monitored because unexpected rows there can hide missing
-- partition definitions.
CREATE TABLE expense_events_default
    PARTITION OF expense_events DEFAULT;

-- Operational tasks commonly include:
-- 1. Create the next partition before data arrives.
-- 2. Monitor partition sizes and query performance.
-- 3. Detach/archive old partitions when retention permits.
-- 4. Keep routing and constraint definitions aligned with application dates.
