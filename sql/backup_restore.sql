-- Day 44 — Backup and Restore Concepts
--
-- Goals:
--   1. Distinguish logical and physical backups.
--   2. Understand full, incremental, and point-in-time recovery concepts.
--   3. Validate backups through restore testing.
--   4. Keep recovery objectives explicit.

-- PostgreSQL logical backup examples (run from a shell, not as SQL):
-- pg_dump -Fc -d app_db -f app_db.dump
-- pg_restore -d app_db_restore app_db.dump
--
-- A plain SQL dump can be created with:
-- pg_dump -d app_db -f app_db.sql
-- psql -d app_db_restore -f app_db.sql

-- Recovery objectives:
-- RPO (Recovery Point Objective): maximum acceptable data loss measured in time.
-- RTO (Recovery Time Objective): maximum acceptable time to restore service.

-- Backup strategy checklist:
-- * Automate backups and monitor their success/failure.
-- * Store backups separately from the primary database infrastructure.
-- * Encrypt backups and restrict access to them.
-- * Retain backups according to recovery and compliance requirements.
-- * Test restores regularly; a successful backup job alone is not proof of recoverability.
-- * Document ownership, recovery steps, and expected restoration time.

-- Point-in-time recovery typically combines a base backup with archived WAL logs.
-- The exact commands depend on the PostgreSQL deployment and backup tooling.
