-- Day 67 — Queue / Event Persistence
-- PostgreSQL-oriented tables for durable event state and a transactional
-- outbox. The message broker remains an application/infrastructure concern.

CREATE TABLE IF NOT EXISTS notification_events (
    event_id BIGSERIAL PRIMARY KEY,
    aggregate_id BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'published', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_notification_events_pending
    ON notification_events(created_at, event_id)
    WHERE status = 'pending';

-- The outbox row and the business-state change should be committed in the
-- same database transaction. A publisher can later claim pending rows and
-- publish them to a broker.

CREATE TABLE IF NOT EXISTS notification_deliveries (
    delivery_id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES notification_events(event_id),
    channel TEXT NOT NULL,
    recipient TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'sent', 'failed')),
    attempt_count INTEGER NOT NULL DEFAULT 0
        CHECK (attempt_count >= 0),
    next_attempt_at TIMESTAMPTZ,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMPTZ,
    UNIQUE (event_id, channel, recipient)
);

CREATE INDEX IF NOT EXISTS idx_notification_deliveries_ready
    ON notification_deliveries(next_attempt_at, delivery_id)
    WHERE status = 'pending';

-- Example transaction boundary:
BEGIN;

INSERT INTO notification_events (
    aggregate_id,
    event_type,
    payload
)
VALUES (
    42,
    'task.completed',
    '{"task_id": 42, "actor_id": 7}'::jsonb
);

-- The application would insert/update its business row in this same
-- transaction. The event must not be published before this transaction
-- commits.

COMMIT;

-- Queue-worker claiming should avoid two workers processing the same row.
-- PostgreSQL workers can use SKIP LOCKED for a bounded batch:
BEGIN;

WITH claimed AS (
    SELECT event_id
    FROM notification_events
    WHERE status = 'pending'
    ORDER BY created_at, event_id
    FOR UPDATE SKIP LOCKED
    LIMIT 100
)
UPDATE notification_events AS e
SET status = 'published',
    published_at = CURRENT_TIMESTAMP
FROM claimed
WHERE e.event_id = claimed.event_id
RETURNING e.event_id, e.event_type, e.payload;

COMMIT;

-- Important design rules:
--   * The database is the durable source of truth for the outbox state.
--   * Broker publication is at-least-once unless the full system provides a
--     stronger guarantee.
--   * Consumers should be idempotent because a published event can be
--     delivered or retried more than once.
--   * Retention and archival policies are required for long-lived outboxes.
--   * SKIP LOCKED improves worker concurrency but does not itself provide
--     exactly-once processing.
