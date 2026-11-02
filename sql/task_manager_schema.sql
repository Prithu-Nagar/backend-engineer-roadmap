-- ============================================================
-- Day 20 — Task Manager Database Design
-- Phase 2 Day 2 — Task Manager MVP schema contract
-- ============================================================
--
-- Core entities:
--   users
--   tasks
--
-- Relationship:
--   One user can own many tasks.
-- ============================================================


-- ------------------------------------------------------------
-- USERS
-- ------------------------------------------------------------

CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_role_check
        CHECK (role IN ('user', 'admin'))
);


-- ------------------------------------------------------------
-- TASKS
-- ------------------------------------------------------------

CREATE TABLE tasks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tasks_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT tasks_title_check
        CHECK (LENGTH(TRIM(title)) > 0),

    CONSTRAINT tasks_status_check
        CHECK (status IN ('pending', 'in_progress', 'completed')),

    CONSTRAINT tasks_priority_check
        CHECK (priority IN ('low', 'medium', 'high'))
);


-- ------------------------------------------------------------
-- INDEXES
-- ------------------------------------------------------------

CREATE INDEX idx_tasks_user_id
ON tasks(user_id);

CREATE INDEX idx_tasks_user_status
ON tasks(user_id, status);

CREATE INDEX idx_tasks_user_priority
ON tasks(user_id, priority);

CREATE INDEX idx_tasks_created_at
ON tasks(created_at);


-- ------------------------------------------------------------
-- SAMPLE DATA
-- ------------------------------------------------------------

-- Sentinel values intentionally cannot authenticate. Replace with real password
-- hashes before using seeded users in an authentication demo.
INSERT INTO users (username, email, password_hash, role)
VALUES
    ('alice', 'alice@example.com', '!seed-password-not-set!', 'user'),
    ('admin', 'admin@example.com', '!seed-password-not-set!', 'admin');


INSERT INTO tasks (
    user_id,
    title,
    description,
    status,
    priority
)
VALUES
    (
        1,
        'Learn Flask',
        'Study application factory patterns.',
        'pending',
        'high'
    ),
    (
        1,
        'Practice DSA',
        'Solve recursion and backtracking problems.',
        'pending',
        'high'
    ),
    (
        2,
        'Review API design',
        'Review modular backend architecture.',
        'completed',
        'medium'
    );


-- ------------------------------------------------------------
-- PRACTICAL QUERIES
-- ------------------------------------------------------------

-- Get all tasks belonging to a user.
SELECT
    id,
    title,
    status,
    priority,
    created_at
FROM tasks
WHERE user_id = 1
ORDER BY created_at DESC;


-- Get pending high-priority tasks.
SELECT
    id,
    title,
    status,
    priority
FROM tasks
WHERE user_id = 1
  AND status = 'pending'
  AND priority = 'high'
ORDER BY created_at DESC;


-- Get tasks together with their owners.
SELECT
    tasks.id,
    tasks.title,
    tasks.priority,
    users.username,
    users.email
FROM tasks
JOIN users
    ON tasks.user_id = users.id
ORDER BY tasks.created_at DESC;