-- Day 63 — Schema Trade-offs
-- PostgreSQL-oriented exercise comparing normalized notification data with
-- denormalized delivery state while keeping ownership and query paths explicit.

CREATE TABLE notification_templates (
    template_id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    channel TEXT NOT NULL,
    body_template TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (channel IN ('email', 'sms', 'push'))
);

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY,
    template_id UUID REFERENCES notification_templates(template_id),
    recipient TEXT NOT NULL,
    subject TEXT,
    body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMPTZ,
    CHECK (status IN ('pending', 'sent', 'failed'))
);

CREATE TABLE notification_deliveries (
    delivery_id UUID PRIMARY KEY,
    notification_id UUID NOT NULL
        REFERENCES notifications(notification_id) ON DELETE CASCADE,
    channel TEXT NOT NULL,
    attempt_count SMALLINT NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending',
    last_error TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (notification_id, channel),
    CHECK (channel IN ('email', 'sms', 'push')),
    CHECK (attempt_count >= 0),
    CHECK (status IN ('pending', 'sent', 'failed'))
);

CREATE INDEX idx_notifications_recipient_created
    ON notifications(recipient, created_at DESC);

CREATE INDEX idx_notifications_status_created
    ON notifications(status, created_at);

CREATE INDEX idx_deliveries_pending
    ON notification_deliveries(updated_at)
    WHERE status = 'pending';

-- Normalized access path: join notification metadata with delivery state.
SELECT
    n.notification_id,
    n.recipient,
    d.channel,
    d.status,
    d.attempt_count
FROM notifications AS n
JOIN notification_deliveries AS d
    ON d.notification_id = n.notification_id
WHERE d.status = 'pending'
ORDER BY d.updated_at;

-- Trade-off notes:
-- 1. Keep templates normalized when many notifications reuse the same content.
-- 2. Keep delivery attempts separate when one notification can use multiple
--    channels or require independent retry state.
-- 3. A denormalized "current_delivery_status" on notifications can reduce a
--    read-time join, but it introduces synchronization complexity.
-- 4. Indexes should follow actual queue and recipient access patterns rather
--    than being added to every column.
