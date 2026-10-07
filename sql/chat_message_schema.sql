-- Day 68: Chat / message schema
-- PostgreSQL-oriented exercise for durable chat history and efficient reads.

CREATE TABLE chat_users (
    user_id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE chat_rooms (
    room_id BIGSERIAL PRIMARY KEY,
    room_type TEXT NOT NULL CHECK (room_type IN ('direct', 'group')),
    created_by BIGINT NOT NULL REFERENCES chat_users(user_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE room_members (
    room_id BIGINT NOT NULL REFERENCES chat_rooms(room_id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES chat_users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_read_message_id BIGINT,
    PRIMARY KEY (room_id, user_id)
);

CREATE TABLE chat_messages (
    message_id BIGSERIAL PRIMARY KEY,
    room_id BIGINT NOT NULL REFERENCES chat_rooms(room_id) ON DELETE CASCADE,
    sender_id BIGINT NOT NULL REFERENCES chat_users(user_id),
    client_message_id UUID NOT NULL,
    body TEXT NOT NULL CHECK (length(body) BETWEEN 1 AND 10000),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    edited_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    UNIQUE (room_id, client_message_id)
);

CREATE INDEX idx_room_members_user
    ON room_members (user_id, room_id);

CREATE INDEX idx_chat_messages_room_time
    ON chat_messages (room_id, created_at DESC, message_id DESC);

CREATE INDEX idx_chat_messages_sender_time
    ON chat_messages (sender_id, created_at DESC);

-- Cursor-based history query. The message_id tie-breaker keeps pagination
-- deterministic when multiple rows share the same timestamp.
-- :room_id, :before_created_at, and :before_message_id are application params.
SELECT message_id, sender_id, body, created_at, edited_at, deleted_at
FROM chat_messages
WHERE room_id = :room_id
  AND (
      created_at < :before_created_at
      OR (
          created_at = :before_created_at
          AND message_id < :before_message_id
      )
  )
ORDER BY created_at DESC, message_id DESC
LIMIT 50;

-- Unread-count query based on the member's last-read cursor.
SELECT COUNT(*) AS unread_count
FROM chat_messages AS m
JOIN room_members AS rm
  ON rm.room_id = m.room_id
 AND rm.user_id = :user_id
WHERE m.room_id = :room_id
  AND m.message_id > COALESCE(rm.last_read_message_id, 0);

-- A production system can move old messages to partitions or archive storage
-- after measuring room size, retention requirements, and query patterns.
