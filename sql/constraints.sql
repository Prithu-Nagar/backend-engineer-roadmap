-- SQL Constraints and Data Integrity
-- PostgreSQL

-- Primary key constraint.
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Foreign key constraint with a relationship to users.
CREATE TABLE tasks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_tasks_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- CHECK constraint to enforce valid values.
ALTER TABLE tasks
ADD CONSTRAINT chk_task_title_not_empty
CHECK (length(trim(title)) > 0);

-- Example of a composite uniqueness constraint.
ALTER TABLE tasks
ADD CONSTRAINT uq_user_task_title
UNIQUE (user_id, title);

-- Parameterized query example.
-- Application code should bind the value instead of
-- constructing SQL by string concatenation.
--
-- SELECT id, title, completed
-- FROM tasks
-- WHERE user_id = $1;
