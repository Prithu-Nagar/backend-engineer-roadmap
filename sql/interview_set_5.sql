-- Day 76: Timed SQL interview set
-- Dialect: PostgreSQL
-- Suggested time: 35 minutes
-- Assumptions: tasks(task_id, user_id, title, status, created_at, completed_at)
--             users(user_id, name, created_at)
--             task_events(event_id, task_id, event_type, occurred_at)
-- Use the actual repository schema if these table/column names differ.

-- 1. Return the five users who created the most tasks.
SELECT
    u.user_id,
    u.name,
    COUNT(t.task_id) AS task_count
FROM users AS u
JOIN tasks AS t ON t.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY task_count DESC, u.user_id
LIMIT 5;

-- 2. Find users who have never created a task.
SELECT u.user_id, u.name
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.user_id
WHERE t.task_id IS NULL
ORDER BY u.user_id;

-- 3. For each user, rank their tasks from newest to oldest.
-- Explain how ROW_NUMBER differs from RANK when timestamps tie.
SELECT
    task_id,
    user_id,
    created_at,
    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY created_at DESC, task_id DESC
    ) AS task_rank
FROM tasks;

-- 4. Return each user's latest task, including ties resolved deterministically.
WITH ranked_tasks AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY created_at DESC, task_id DESC
        ) AS row_num
    FROM tasks AS t
)
SELECT task_id, user_id, title, status, created_at
FROM ranked_tasks
WHERE row_num = 1
ORDER BY user_id;

-- 5. Calculate the number of tasks created per day for the last 30 days.
SELECT
    created_at::date AS task_date,
    COUNT(*) AS tasks_created
FROM tasks
WHERE created_at >= CURRENT_DATE - INTERVAL '29 days'
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
GROUP BY created_at::date
ORDER BY task_date;

-- 6. Find tasks that have more than three recorded events.
SELECT task_id, COUNT(*) AS event_count
FROM task_events
GROUP BY task_id
HAVING COUNT(*) > 3
ORDER BY event_count DESC, task_id;

-- 7. Find completed tasks whose completion time precedes creation time.
-- Explain why this query is useful as a data-quality check.
SELECT task_id, user_id, created_at, completed_at
FROM tasks
WHERE status = 'completed'
  AND completed_at < created_at
ORDER BY task_id;

-- 8. Discussion: propose an index for a query filtering by user_id and
-- ordering by created_at DESC. Explain selectivity, write overhead, and
-- how you would validate the index with EXPLAIN (ANALYZE, BUFFERS).
