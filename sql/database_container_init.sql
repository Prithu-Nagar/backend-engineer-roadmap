-- ============================================================
-- Day 41 — Database Container Initialization
-- ============================================================
--
-- This script is intended for a PostgreSQL container's
-- initialization directory (for example, /docker-entrypoint-initdb.d).
--
-- Initialization scripts run when the database is first created.
-- They should be safe to understand as schema/bootstrap steps rather
-- than as application-level migration history.
-- ============================================================


-- ------------------------------------------------------------
-- USERS
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_role_check
        CHECK (role IN ('user', 'admin'))
);


-- ------------------------------------------------------------
-- TASKS
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tasks_title_check
        CHECK (LENGTH(TRIM(title)) > 0),

    CONSTRAINT tasks_priority_check
        CHECK (priority IN ('low', 'medium', 'high'))
);


-- ------------------------------------------------------------
-- INDEXES
-- ------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_tasks_user_id
ON tasks(user_id);

CREATE INDEX IF NOT EXISTS idx_tasks_user_completed
ON tasks(user_id, completed);


-- ------------------------------------------------------------
-- SEED DATA
-- ------------------------------------------------------------

INSERT INTO users (username, email, role)
VALUES
    ('alice', 'alice@example.com', 'user'),
    ('admin', 'admin@example.com', 'admin')
ON CONFLICT (username) DO NOTHING;


INSERT INTO tasks (user_id, title, description, priority, completed)
SELECT
    users.id,
    seed.title,
    seed.description,
    seed.priority,
    seed.completed
FROM users
CROSS JOIN (
    VALUES
        (
            'alice',
            'Containerize Task Manager',
            'Build and run the backend image.',
            'high',
            FALSE
        ),
        (
            'alice',
            'Practice weighted graphs',
            'Review Dijkstra and minimax path reasoning.',
            'medium',
            FALSE
        )
) AS seed(username, title, description, priority, completed)
WHERE users.username = seed.username
  AND NOT EXISTS (
      SELECT 1
      FROM tasks
      WHERE tasks.user_id = users.id
        AND tasks.title = seed.title
  );
