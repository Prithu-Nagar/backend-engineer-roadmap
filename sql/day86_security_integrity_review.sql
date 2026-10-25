-- Day 86 — Security and data-integrity review
-- PostgreSQL examples. Review roles, object names, and migration effects before execution.

-- 1. Inspect privileges granted to application roles.
SELECT grantee, table_schema, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public'
ORDER BY grantee, table_name, privilege_type;

-- 2. Apply least privilege to a dedicated runtime role (adapt role/table names).
-- Run as an appropriately privileged database administrator.
REVOKE ALL ON TABLE public.tasks FROM PUBLIC;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.tasks TO task_app;

-- 3. Integrity constraints should be enforced by the database, not only the API.
-- Check for existing violations before adding constraints in a migration.
SELECT task_id, user_id
FROM public.tasks
WHERE user_id IS NULL;

-- Example migration statements; validate existing data and deploy in a controlled migration.
-- ALTER TABLE public.tasks ALTER COLUMN user_id SET NOT NULL;
-- ALTER TABLE public.tasks ADD CONSTRAINT tasks_title_nonempty CHECK (length(trim(title)) > 0);

-- 4. Parameterized statements prevent values from becoming executable SQL.
-- Application example: SELECT task_id FROM public.tasks WHERE user_id = %s AND task_id = %s;

-- 5. Review row-level security only after policies are defined and tested.
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Review checklist:
-- - Runtime credentials cannot create roles, databases, or schemas unless necessary.
-- - Secrets are not stored in SQL scripts, logs, or source control.
-- - Authorization predicates include tenant/user ownership.
-- - Constraints and transactions protect invariants under concurrent requests.
-- - Backups, restore tests, and migration rollback plans are documented.
