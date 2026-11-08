-- URL Shortener relational schema.
--
-- This PostgreSQL schema mirrors the canonical Django/DRF model. The
-- short_code unique constraint is the concurrency-safe collision boundary.
-- The owner FK targets Django's default auth_user table.

CREATE TABLE url_shortener_shorturl (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT REFERENCES auth_user(id) ON DELETE CASCADE,
    short_code VARCHAR(32) NOT NULL UNIQUE,
    original_url VARCHAR(2048) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    click_count BIGINT NOT NULL DEFAULT 0 CHECK (click_count >= 0),

    CONSTRAINT shorturl_original_url_not_empty
        CHECK (length(trim(original_url)) > 0),

    CONSTRAINT shorturl_short_code_not_empty
        CHECK (length(trim(short_code)) > 0),

    CONSTRAINT shorturl_expiry_after_creation
        CHECK (expires_at IS NULL OR expires_at > created_at)
);

CREATE INDEX idx_url_shortener_shorturl_owner_created
    ON url_shortener_shorturl (owner_id, created_at DESC);

CREATE INDEX idx_url_shortener_shorturl_active_expiry
    ON url_shortener_shorturl (is_active, expires_at);
