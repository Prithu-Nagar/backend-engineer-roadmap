-- Day 61 — Task Manager Schema Design
-- PostgreSQL-oriented relational model for an LLD-focused Task Manager.

CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    owner_id UUID NOT NULL REFERENCES users(user_id),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (owner_id, name)
);

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    assignee_id UUID REFERENCES users(user_id),
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'todo',
    priority SMALLINT NOT NULL DEFAULT 3,
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('todo', 'in_progress', 'done')),
    CHECK (priority BETWEEN 1 AND 5)
);

CREATE TABLE task_dependencies (
    task_id UUID NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    depends_on_task_id UUID NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, depends_on_task_id),
    CHECK (task_id <> depends_on_task_id)
);

CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX idx_tasks_assignee_status ON tasks(assignee_id, status);
CREATE INDEX idx_tasks_due_at ON tasks(due_at) WHERE status <> 'done';
CREATE INDEX idx_task_dependencies_dependency
    ON task_dependencies(depends_on_task_id);

-- Typical access pattern: active tasks for one project, ordered for display.
SELECT task_id, title, status, priority, due_at
FROM tasks
WHERE project_id = $1
  AND status <> 'done'
ORDER BY priority, due_at NULLS LAST, created_at;
