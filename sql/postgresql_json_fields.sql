-- Day 27 — PostgreSQL-Oriented Features: JSON / JSONB
--
-- PostgreSQL's JSONB type is useful when a relational schema needs to retain
-- flexible structured attributes while still supporting indexing and queries.

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    profile JSONB NOT NULL DEFAULT '{}'::jsonb
);

INSERT INTO users (name, profile)
VALUES
    ('Alice', '{"department": "engineering", "skills": ["python", "sql"]}'),
    ('Bob', '{"department": "product", "skills": ["analytics"]}');

-- Access a JSON field.
SELECT
    id,
    name,
    profile->>'department' AS department
FROM users;

-- Filter rows by a JSON value.
SELECT id, name
FROM users
WHERE profile->>'department' = 'engineering';

-- Check whether a JSONB document contains a structure.
SELECT id, name
FROM users
WHERE profile @> '{"department": "engineering"}';

-- Index JSONB containment and related queries.
CREATE INDEX idx_users_profile_gin
ON users
USING GIN (profile);

-- Query an array stored inside JSONB.
SELECT id, name
FROM users
WHERE profile->'skills' ? 'python';

-- Update one JSONB attribute while preserving the rest of the document.
UPDATE users
SET profile = jsonb_set(profile, '{department}', '"platform"')
WHERE id = 1;

-- JSON should complement relational modeling rather than replace strongly
-- structured columns that require constraints, joins, or frequent indexing.
