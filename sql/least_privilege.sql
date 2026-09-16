-- Day 47 — Least-Privilege Database Access
--
-- Grant only the database capabilities required by each application role.
-- Adapt role names, schemas, and table names to the deployment environment.

-- 1. Create separate roles for application runtime and read-only reporting.
CREATE ROLE task_manager_app LOGIN PASSWORD 'REPLACE_IN_SECRET_MANAGER';
CREATE ROLE task_manager_readonly LOGIN PASSWORD 'REPLACE_IN_SECRET_MANAGER';

-- 2. Prevent roles from creating objects in the shared public schema.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM task_manager_app;
REVOKE ALL ON SCHEMA public FROM task_manager_readonly;

-- 3. Allow the application role to use a dedicated application schema.
GRANT USAGE ON SCHEMA task_manager TO task_manager_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA task_manager
    TO task_manager_app;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA task_manager
    TO task_manager_app;

-- 4. Give reporting access only to reads.
GRANT USAGE ON SCHEMA task_manager TO task_manager_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA task_manager TO task_manager_readonly;

-- 5. Ensure future tables inherit the intended defaults.
ALTER DEFAULT PRIVILEGES IN SCHEMA task_manager
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO task_manager_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA task_manager
    GRANT SELECT ON TABLES TO task_manager_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA task_manager
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO task_manager_app;

-- 6. Explicitly avoid granting administrative capabilities to the app role.
-- Do not grant CREATEDB, CREATEROLE, SUPERUSER, or broad database ownership
-- privileges to the runtime role.

-- 7. Verify effective privileges during deployment review.
-- SELECT grantee, table_schema, table_name, privilege_type
-- FROM information_schema.role_table_grants
-- WHERE grantee IN ('task_manager_app', 'task_manager_readonly')
-- ORDER BY grantee, table_schema, table_name, privilege_type;
