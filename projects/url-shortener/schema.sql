-- Day 21 — URL Shortener Schema
--
-- PostgreSQL-oriented initial schema.
-- The schema keeps the short code unique and stores lifecycle metadata.

CREATE TABLE short_urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(32) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT short_urls_original_url_not_empty
        CHECK (length(trim(original_url)) > 0),

    CONSTRAINT short_urls_short_code_not_empty
        CHECK (length(trim(short_code)) > 0),

    CONSTRAINT short_urls_expiry_after_creation
        CHECK (expires_at IS NULL OR expires_at > created_at)
);

CREATE INDEX idx_short_urls_active
    ON short_urls (is_active);

CREATE INDEX idx_short_urls_expires_at
    ON short_urls (expires_at);
