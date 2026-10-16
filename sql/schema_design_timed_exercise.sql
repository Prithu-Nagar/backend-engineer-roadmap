-- Day 77: Timed schema-design interview exercise
-- Dialect: PostgreSQL
-- Suggested time: 35 minutes
-- Goal: design a schema for a multi-user chat service before writing queries.
-- Requirements:
--   1. A user can belong to many conversations.
--   2. A conversation has many messages, each authored by one user.
--   3. Membership records track when a user joined and their last-read time.
--   4. Message retries must be idempotent per sender.
--   5. Conversation history is commonly read newest-first, with stable pagination.
--
-- Task A: Write CREATE TABLE statements for users, conversations,
-- conversation_members, and messages. Add primary keys, foreign keys,
-- NOT NULL constraints, appropriate CHECK constraints, and uniqueness rules.
--
-- Task B: Add indexes for:
--   - listing conversations for a user;
--   - reading messages for one conversation newest-first;
--   - preventing duplicate client_message_id values per sender.
--
-- Task C: Explain:
--   - why membership is a junction table;
--   - whether message deletion should cascade;
--   - how you would represent edited/deleted messages;
--   - how keyset pagination differs from OFFSET pagination;
--   - how you would migrate a large table without a long blocking lock.
--
-- Reference design (adapt constraints to product requirements).

CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE conversations (
    conversation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT,
    created_by BIGINT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE conversation_members (
    conversation_id BIGINT NOT NULL
        REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL
        REFERENCES users(user_id) ON DELETE RESTRICT,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_read_at TIMESTAMPTZ,
    PRIMARY KEY (conversation_id, user_id),
    CHECK (last_read_at IS NULL OR last_read_at >= joined_at)
);

CREATE TABLE messages (
    message_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id BIGINT NOT NULL
        REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    client_message_id TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    edited_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    UNIQUE (sender_id, client_message_id),
    CHECK (edited_at IS NULL OR edited_at >= created_at),
    CHECK (deleted_at IS NULL OR deleted_at >= created_at)
);

CREATE INDEX idx_conversation_members_user
    ON conversation_members (user_id, conversation_id);

CREATE INDEX idx_messages_conversation_created
    ON messages (conversation_id, created_at DESC, message_id DESC);

-- Keyset pagination example: use the final (created_at, message_id)
-- pair from the previous page as the cursor.
-- SELECT message_id, sender_id, body, created_at
-- FROM messages
-- WHERE conversation_id = $1
--   AND (created_at, message_id) < ($2, $3)
-- ORDER BY created_at DESC, message_id DESC
-- LIMIT 50;
--
-- Review note: a production design should validate that the sender is a
-- member of the conversation in the write path, and define retention,
-- moderation, privacy, and deletion requirements explicitly.
