-- Day 62 — Expense Tracker Relational Modeling
-- PostgreSQL-oriented LLD exercise for explicit entities, relationships,
-- constraints, and access paths.

CREATE TABLE expense_categories (
    category_id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expenses (
    expense_id UUID PRIMARY KEY,
    category_id UUID NOT NULL REFERENCES expense_categories(category_id),
    amount NUMERIC(12, 2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (amount > 0)
);

CREATE TABLE expense_tags (
    tag_id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE expense_tag_links (
    expense_id UUID NOT NULL REFERENCES expenses(expense_id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES expense_tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (expense_id, tag_id)
);

CREATE INDEX idx_expenses_category_date
    ON expenses(category_id, expense_date DESC);

CREATE INDEX idx_expenses_date
    ON expenses(expense_date DESC);

CREATE INDEX idx_expense_tag_links_tag
    ON expense_tag_links(tag_id, expense_id);

-- Common access pattern: category totals for a date range.
SELECT
    c.name AS category,
    SUM(e.amount) AS total_amount
FROM expenses AS e
JOIN expense_categories AS c
    ON c.category_id = e.category_id
WHERE e.expense_date >= $1
  AND e.expense_date < $2
GROUP BY c.category_id, c.name
ORDER BY total_amount DESC, category;

-- LLD modeling notes:
-- 1. Categories are normalized into their own entity.
-- 2. Tags use a many-to-many relationship instead of repeated text values.
-- 3. Monetary values use NUMERIC rather than floating-point storage.
-- 4. Foreign keys preserve relationship integrity.
-- 5. Composite indexes match common category/date access patterns.
