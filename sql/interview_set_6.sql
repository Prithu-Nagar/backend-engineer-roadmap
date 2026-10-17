-- Day 78: Mixed SQL interview set
-- Dialect: PostgreSQL
-- Suggested time: 35 minutes
-- Assumptions: users(user_id, name, created_at)
--             tasks(task_id, user_id, title, status, created_at, completed_at)
--             task_events(event_id, task_id, event_type, occurred_at)
-- Verify names against the target schema before running.

-- 1. Return each user's total task count, including users with no tasks.
SELECT
    u.user_id,
    u.name,
    COUNT(t.task_id) AS task_count
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY task_count DESC, u.user_id;

-- 2. Find users whose task count is above the average task count per user.
WITH task_counts AS (
    SELECT u.user_id, COUNT(t.task_id) AS task_count
    FROM users AS u
    LEFT JOIN tasks AS t ON t.user_id = u.user_id
    GROUP BY u.user_id
)
SELECT user_id, task_count
FROM task_counts
WHERE task_count > (SELECT AVG(task_count) FROM task_counts)
ORDER BY task_count DESC, user_id;

-- 3. Find the latest task for each user using a window function.
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.user_id
            ORDER BY t.created_at DESC, t.task_id DESC
        ) AS row_num
    FROM tasks AS t
)
SELECT task_id, user_id, title, status, created_at
FROM ranked
WHERE row_num = 1
ORDER BY user_id;

-- 4. Calculate completion rate per user; avoid division by zero.
SELECT
    u.user_id,
    u.name,
    COUNT(t.task_id) AS total_tasks,
    COUNT(t.task_id) FILTER (WHERE t.status = 'completed') AS completed_tasks,
    ROUND(
        100.0 * COUNT(t.task_id) FILTER (WHERE t.status = 'completed')
        / NULLIF(COUNT(t.task_id), 0),
        2
    ) AS completion_percentage
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY u.user_id;

-- 5. Find tasks that have no recorded events.
SELECT t.task_id, t.title
FROM tasks AS t
WHERE NOT EXISTS (
    SELECT 1
    FROM task_events AS e
    WHERE e.task_id = t.task_id
)
ORDER BY t.task_id;

-- 6. Return daily task creation counts for the last 14 days.
SELECT created_at::date AS task_date, COUNT(*) AS task_count
FROM tasks
WHERE created_at >= CURRENT_DATE - INTERVAL '13 days'
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
GROUP BY created_at::date
ORDER BY task_date;

-- 7. Discussion: propose an index for a user's newest tasks.
-- Compare (user_id, created_at DESC, task_id DESC) with an index on
-- created_at alone. Explain selectivity, sort avoidance, and write overhead.
-- Validate with EXPLAIN (ANALYZE, BUFFERS) on representative data.

-- 8. Discussion: two requests attempt to complete the same task concurrently.
-- Explain transaction boundaries, allowed state transitions, and whether
-- optimistic locking or SELECT ... FOR UPDATE is appropriate.
