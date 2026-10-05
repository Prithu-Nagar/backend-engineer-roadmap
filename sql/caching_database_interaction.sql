-- Day 66 — Caching and Database Interaction
-- PostgreSQL-oriented examples for a cache-aside read path and a safe write
-- path. The cache itself is represented by pseudocode comments because Redis
-- is an application dependency rather than a PostgreSQL table.

CREATE TABLE IF NOT EXISTS product_catalog (
    product_id BIGSERIAL PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_product_catalog_active_updated
    ON product_catalog(is_active, updated_at DESC);

-- Cache-aside read flow:
--   1. Application checks cache key product:{product_id}.
--   2. On a hit, return the cached representation if it is still valid.
--   3. On a miss, query the database.
--   4. Populate the cache with a bounded TTL.
--   5. Return the database result.
--
-- SQL for the database fallback:
SELECT
    product_id,
    sku,
    name,
    price,
    is_active,
    updated_at
FROM product_catalog
WHERE product_id = 42;

-- A cache should not become the source of truth for durable product state.
-- Database constraints remain authoritative for uniqueness and validity.

-- Example update transaction:
BEGIN;

UPDATE product_catalog
SET
    price = 1499.00,
    updated_at = CURRENT_TIMESTAMP
WHERE product_id = 42
  AND is_active = TRUE;

COMMIT;

-- Application-level write policy after a successful commit:
--   1. Do not update the cache before the database commit succeeds.
--   2. Invalidate product:42 after commit, or write the new representation
--      when the cache contract guarantees that the value is complete.
--   3. A subsequent read repopulates the cache from the committed database
--      state.
--
-- This ordering avoids exposing a cache value for a transaction that later
-- rolls back.

-- Prevent stale cache entries from living forever. The TTL is a safety bound,
-- not a substitute for explicit invalidation when data changes.

-- For list queries, cache keys must include every input that changes the
-- result, such as filters, sort order, and pagination parameters.
SELECT
    product_id,
    sku,
    name,
    price
FROM product_catalog
WHERE is_active = TRUE
ORDER BY updated_at DESC, product_id DESC
LIMIT 50;

-- Interaction rules to review during design:
--   * Cache hit ratio should be measured, not assumed.
--   * Cache misses must degrade to a bounded database path.
--   * Negative caching needs a short TTL so newly-created records appear.
--   * Cache stampedes can be reduced with request coalescing or jittered TTLs.
--   * Replica reads must account for replica lag before being used for a
--     read-after-write workflow.
--   * Cache serialization must preserve the API contract and invalidation
--     policy.
