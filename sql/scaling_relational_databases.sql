-- Day 65 — Scaling Relational Databases
-- PostgreSQL-oriented exercise for a URL Shortener workload.
-- The examples focus on access paths, read scaling, partitioning, and
-- operational safeguards rather than assuming that every workload needs
-- sharding immediately.

CREATE TABLE IF NOT EXISTS url_events (
    event_id BIGSERIAL PRIMARY KEY,
    short_code TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    client_region TEXT,
    latency_ms INTEGER CHECK (latency_ms >= 0)
);

-- Keep the redirect lookup index aligned with the primary read path.
CREATE INDEX IF NOT EXISTS idx_url_events_code_time
    ON url_events(short_code, occurred_at DESC);

-- A time-partitioned event table can isolate recent writes from historical
-- data when event volume becomes large enough to justify the operational cost.
CREATE TABLE IF NOT EXISTS url_events_partitioned (
    event_id BIGSERIAL,
    short_code TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    client_region TEXT,
    latency_ms INTEGER CHECK (latency_ms >= 0),
    PRIMARY KEY (event_id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE IF NOT EXISTS url_events_2026_10
    PARTITION OF url_events_partitioned
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

CREATE INDEX IF NOT EXISTS idx_url_events_2026_10_code_time
    ON url_events_2026_10(short_code, occurred_at DESC);

-- Query shape that should remain index-friendly for recent analytics.
SELECT
    short_code,
    COUNT(*) AS redirect_count,
    AVG(latency_ms) AS average_latency_ms
FROM url_events_partitioned
WHERE occurred_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY short_code
ORDER BY redirect_count DESC
LIMIT 100;

-- Read-replica routing is an application concern. A typical policy is:
--   1. Primary: writes and reads that require read-after-write guarantees.
--   2. Replica: analytics and eventually-consistent read-heavy workloads.
--   3. Cache: hot redirect lookups with an explicit TTL/invalidation policy.
--
-- Do not route every SELECT to replicas blindly. Replica lag can make a
-- recently-created URL temporarily invisible to a user that expects the
-- create-then-read flow to be immediately consistent.

-- Operational checks should be based on measured workload characteristics:
--   * query latency and buffer/cache hit ratio
--   * connection utilization
--   * replica replay lag
--   * table/index growth
--   * lock waits and transaction duration
--   * CPU and I/O saturation

-- Scaling progression:
--   1. Fix inefficient queries and indexes.
--   2. Add connection pooling and bound concurrency.
--   3. Add caching for proven hot reads.
--   4. Add read replicas for suitable read-heavy workloads.
--   5. Partition very large tables by a stable access dimension such as time.
--   6. Consider sharding only when a single database has become the measured
--      bottleneck and the access pattern supports a clear shard key.
