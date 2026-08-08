-- Query Optimization Examples
-- PostgreSQL

-- Select only the columns required by the application.
SELECT id, title, completed
FROM tasks
WHERE user_id = 10;

-- Index a column frequently used for filtering.
CREATE INDEX idx_tasks_user_id
ON tasks(user_id);

-- Composite index for queries filtering by both columns.
CREATE INDEX idx_tasks_user_completed
ON tasks(user_id, completed);

-- Inspect the query execution plan.
EXPLAIN
SELECT id, title, completed
FROM tasks
WHERE user_id = 10
AND completed = false;

-- Inspect the actual execution plan.
EXPLAIN ANALYZE
SELECT id, title, completed
FROM tasks
WHERE user_id = 10
AND completed = false;
