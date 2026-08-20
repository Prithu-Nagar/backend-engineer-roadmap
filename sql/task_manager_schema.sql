-- ============================================================
-- Day 20 — Task Manager Database Design
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
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tasks_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT tasks_title_check
        CHECK (LENGTH(TRIM(title)) > 0),

    CONSTRAINT tasks_priority_check
        CHECK (priority IN ('low', 'medium', 'high'))
);


-- ------------------------------------------------------------
-- INDEXES
-- ------------------------------------------------------------

CREATE INDEX idx_tasks_user_id
ON tasks(user_id);

CREATE INDEX idx_tasks_user_completed
ON tasks(user_id, completed);

CREATE INDEX idx_tasks_user_priority
ON tasks(user_id, priority);

CREATE INDEX idx_tasks_created_at
ON tasks(created_at);


-- ------------------------------------------------------------
-- SAMPLE DATA
-- ------------------------------------------------------------

INSERT INTO users (username, email, role)
VALUES
    ('alice', 'alice@example.com', 'user'),
    ('admin', 'admin@example.com', 'admin');


INSERT INTO tasks (
    user_id,
    title,
    description,
    priority,
    completed
)
VALUES
    (
        1,
        'Learn Flask',
        'Study application factory patterns.',
        'high',
        FALSE
    ),
    (
        1,
        'Practice DSA',
        'Solve recursion and backtracking problems.',
        'high',
        FALSE
    ),
    (
        2,
        'Review API design',
        'Review modular backend architecture.',
        'medium',
        TRUE
    );


-- ------------------------------------------------------------
-- PRACTICAL QUERIES
-- ------------------------------------------------------------

-- Get all tasks belonging to a user.
SELECT
    id,
    title,
    priority,
    completed,
    created_at
FROM tasks
WHERE user_id = 1
ORDER BY created_at DESC;


-- Get pending high-priority tasks.
SELECT
    id,
    title,
    priority
FROM tasks
WHERE user_id = 1
  AND completed = FALSE
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