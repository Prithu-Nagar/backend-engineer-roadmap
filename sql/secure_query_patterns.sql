-- Day 48 — Secure Query Patterns & Parameterization
--
-- Prefer bound parameters for user-controlled values.
-- The examples use PostgreSQL-style positional parameters ($1, $2, ...).

-- 1. Safe value filtering: the database driver binds the value separately.
SELECT id, title, status
FROM tasks
WHERE owner_id = $1
  AND status = $2;

-- 2. Safe prefix search: the pattern is still a bound value.
SELECT id, title
FROM tasks
WHERE title ILIKE $1
ORDER BY id
LIMIT $2;

-- 3. Safe pagination values should also be bound.
SELECT id, title, created_at
FROM tasks
WHERE owner_id = $1
ORDER BY created_at DESC, id DESC
LIMIT $2 OFFSET $3;

-- 4. Do not build SQL by concatenating request values.
-- Unsafe:
-- SELECT * FROM tasks WHERE owner_id = '...request value...';

-- 5. Identifiers such as table or column names cannot normally be bound as
-- value parameters. Validate them against an allow-list and quote them with
-- database-specific identifier functions when dynamic SQL is unavoidable.
--
-- Example PostgreSQL PL/pgSQL pattern:
--
-- EXECUTE format(
--     'SELECT id, title FROM %I WHERE owner_id = $1',
--     validated_table_name
-- )
-- USING owner_id;

-- 6. Parameterization protects values; authorization still has to be enforced.
-- A correctly parameterized query can still expose another user's rows if the
-- application fails to constrain the query by the authenticated owner.

-- 7. Keep privileged database credentials out of application source code.
-- Combine parameterization with least-privilege roles from Day 47.
