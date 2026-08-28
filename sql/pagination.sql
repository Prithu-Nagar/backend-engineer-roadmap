-- Day 17 - SQL Pagination
-- Topics:
-- OFFSET pagination
-- Keyset/cursor pagination
-- Stable ordering
-- Pagination trade-offs

-- ---------------------------------------------------------
-- Example table
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL
);

-- ---------------------------------------------------------
-- OFFSET pagination
-- ---------------------------------------------------------

-- Page 1, 20 rows
SELECT id, title, completed, created_at
FROM tasks
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 0;

-- Page 2, 20 rows
SELECT id, title, completed, created_at
FROM tasks
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 20;

-- OFFSET is simple, but large offsets can become expensive because
-- the database may need to walk past many rows before returning the page.

-- ---------------------------------------------------------
-- Keyset / cursor pagination
-- ---------------------------------------------------------

-- Assume the previous page ended at:
-- created_at = '2026-08-17 10:00:00'
-- id = 120

SELECT id, title, completed, created_at
FROM tasks
WHERE (created_at, id) < ('2026-08-17 10:00:00', 120)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Keyset pagination uses the last item from the previous page as
-- the cursor for the next page.

-- ---------------------------------------------------------
-- Filtering + pagination
-- ---------------------------------------------------------

SELECT id, title, completed, created_at
FROM tasks
WHERE completed = FALSE
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 40;

-- ---------------------------------------------------------
-- Pagination design notes
-- ---------------------------------------------------------

/*
OFFSET pagination:
- Simple API semantics.
- Easy to jump directly to a page number.
- Can become slower with large offsets.
- Results can shift when rows are inserted/deleted between requests.

Keyset/cursor pagination:
- Uses a stable ordering and a cursor from the previous page.
- Usually performs better for deep pagination.
- Better suited to large or frequently changing datasets.
- Does not naturally support arbitrary page-number jumps.

For stable ordering, include a unique tie-breaker such as `id`.
*/

-- ---------------------------------------------------------
-- Day 28 - Advanced pagination and query patterns
-- ---------------------------------------------------------

-- A stable, unique ordering is important for both OFFSET and cursor
-- pagination. The unique id acts as a tie-breaker when timestamps match.

-- Cursor pagination with a composite ordering key.
-- Previous cursor: created_at = '2026-08-28 09:00:00', id = 250
SELECT id, title, completed, created_at
FROM tasks
WHERE (created_at, id) < ('2026-08-28 09:00:00', 250)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Filtering should be applied before pagination so the cursor describes
-- the same ordered result set as the current request.
SELECT id, title, completed, created_at
FROM tasks
WHERE completed = FALSE
  AND (created_at, id) < ('2026-08-28 09:00:00', 250)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Count metadata is useful when the API needs a total count, but COUNT(*)
-- can add cost on large filtered datasets. Do not calculate it automatically
-- when the API contract only requires next/previous cursor information.
SELECT COUNT(*) AS total
FROM tasks
WHERE completed = FALSE;

-- Example of a safe query pattern for optional filters:
-- Build SQL with parameterized values in application code. Do not concatenate
-- user-supplied filter values directly into the SQL string.
SELECT id, title, completed, created_at
FROM tasks
WHERE completed = :completed
ORDER BY created_at DESC, id DESC
LIMIT :limit_value;

/*
Day 28 design notes:

- Use OFFSET when simple page-number navigation is more important than deep-page performance.
- Prefer keyset/cursor pagination for large, frequently changing datasets.
- Always define a deterministic ordering, normally with a unique tie-breaker.
- Keep the cursor tied to the same filters and ordering used by the query.
- Avoid exposing database offsets or raw SQL fragments as trusted client input.
- Parameterize filter values and validate sort fields against an allowlist.
- Only request total counts when the API actually needs them.
- Index the columns used by the WHERE + ORDER BY pattern when the workload justifies it.
*/

