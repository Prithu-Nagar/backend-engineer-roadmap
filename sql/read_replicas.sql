-- Day 35 — Read Replicas & Replication Lag
--
-- Read replicas can scale read-heavy workloads, but asynchronous replication
-- means a replica may temporarily lag behind the primary.

-- Primary: writes are committed here.
INSERT INTO expenses (id, category, amount, expense_date)
VALUES (1001, 'travel', 2500.00, DATE '2026-09-04');

-- Application read routing is commonly split by consistency requirement:
--   Strongly consistent read -> primary
--   Eventually consistent read -> replica
--
-- The following queries represent the same logical read on either side.
SELECT id, category, amount, expense_date
FROM expenses
WHERE id = 1001;

-- A replica can be monitored for replay progress. PostgreSQL exposes WAL
-- positions and replay timestamps from the replica's recovery functions.
SELECT pg_is_in_recovery() AS is_replica,
       pg_last_wal_receive_lsn() AS received_lsn,
       pg_last_wal_replay_lsn() AS replayed_lsn,
       pg_last_xact_replay_timestamp() AS last_replay_timestamp;

-- A simplified lag estimate can be derived from the last replay timestamp.
SELECT EXTRACT(EPOCH FROM (clock_timestamp() - pg_last_xact_replay_timestamp()))
       AS replay_lag_seconds;

-- Routing guidance:
-- 1. Send writes and read-after-write requests to the primary when needed.
-- 2. Send tolerant, read-heavy traffic to replicas.
-- 3. Monitor replica lag and remove unhealthy replicas from read routing.
-- 4. Do not assume a successful write is immediately visible on every replica.
