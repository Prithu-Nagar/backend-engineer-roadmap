-- Day 64 — Database-per-Service Schema
-- PostgreSQL-oriented exercise showing ownership boundaries for a URL
-- Shortener split into URL and identity concerns.

CREATE SCHEMA IF NOT EXISTS url_service;
CREATE SCHEMA IF NOT EXISTS identity_service;

CREATE TABLE identity_service.users (
    user_id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE url_service.short_urls (
    short_url_id UUID PRIMARY KEY,
    short_code TEXT NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    owner_user_id UUID NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ
);

CREATE INDEX idx_short_urls_owner_created
    ON url_service.short_urls(owner_user_id, created_at DESC);

CREATE INDEX idx_short_urls_active_code
    ON url_service.short_urls(short_code)
    WHERE is_active = TRUE;

-- The URL service stores the external owner identifier but does not create
-- a foreign key into identity_service.users. Cross-service ownership is an
-- application/service boundary rather than a database-level relationship.

-- URL-service-owned query:
SELECT
    short_code,
    original_url,
    expires_at
FROM url_service.short_urls
WHERE short_code = $1
  AND is_active = TRUE;

-- Local ownership check can be performed against the URL service's own data.
-- If user details are needed, the URL service should call the identity
-- service or consume an authorized user projection/event rather than query
-- identity_service.users directly.

-- Trade-off notes:
-- 1. Each service owns its tables, migrations, and access patterns.
-- 2. Cross-service joins are intentionally avoided.
-- 3. Duplicated identifiers or read projections may become eventually
--    consistent and must have an explicit source of truth.
-- 4. Distributed workflows should prefer idempotency, events, an outbox, or
--    compensating actions instead of assuming a shared database transaction.
