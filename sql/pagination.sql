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