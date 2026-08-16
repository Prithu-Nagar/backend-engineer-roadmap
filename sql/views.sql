-- Day 16 - SQL Views
-- Topics:
-- Views
-- Materialized-view concept
-- When to use views
-- Views vs materialized views

-- ---------------------------------------------------------
-- Example tables
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------------------------------------
-- Regular VIEW
-- ---------------------------------------------------------

CREATE VIEW user_task_summary AS
SELECT
    u.id AS user_id,
    u.name AS user_name,
    COUNT(t.id) AS total_tasks,
    SUM(
        CASE
            WHEN t.completed = TRUE THEN 1
            ELSE 0
        END
    ) AS completed_tasks
FROM users u
LEFT JOIN tasks t
    ON u.id = t.user_id
GROUP BY
    u.id,
    u.name;

-- Query the view
SELECT *
FROM user_task_summary;

-- ---------------------------------------------------------
-- Example filtered query using the VIEW
-- ---------------------------------------------------------

SELECT
    user_id,
    user_name,
    total_tasks,
    completed_tasks
FROM user_task_summary
WHERE total_tasks > 5;

-- ---------------------------------------------------------
-- Materialized VIEW concept
-- ---------------------------------------------------------

/*
A regular VIEW stores the query definition.

A materialized VIEW stores the result of the query.

Conceptually:

Regular VIEW:

    Query
      ↓
   Database
      ↓
   Calculate result

Materialized VIEW:

    Query
      ↓
   Calculate
      ↓
   Store result
      ↓
   Read stored result

The materialized result must be refreshed when the underlying
data changes.

Exact syntax depends on the database engine.
*/