-- Day 56 — Conversation / Session Persistence
-- PostgreSQL-oriented schema for persisting AI conversation state and
-- individual messages without coupling the database to a model provider.

CREATE TABLE IF NOT EXISTS agent_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    tenant_id BIGINT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    context_version INTEGER NOT NULL DEFAULT 1,
    summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('active', 'archived', 'expired'))
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
    sequence_no INTEGER NOT NULL,
    role VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER,
    tool_name VARCHAR(128),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (role IN ('system', 'user', 'assistant', 'tool')),
    CHECK (sequence_no > 0),
    UNIQUE (session_id, sequence_no)
);

CREATE TABLE IF NOT EXISTS session_context_snapshots (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
    context_version INTEGER NOT NULL,
    summary TEXT,
    memory JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (session_id, context_version)
);

CREATE INDEX IF NOT EXISTS idx_agent_sessions_user_updated
    ON agent_sessions (user_id, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_agent_sessions_tenant_status
    ON agent_sessions (tenant_id, status);

CREATE INDEX IF NOT EXISTS idx_conversation_messages_session_sequence
    ON conversation_messages (session_id, sequence_no);

CREATE INDEX IF NOT EXISTS idx_conversation_messages_session_created
    ON conversation_messages (session_id, created_at);

CREATE INDEX IF NOT EXISTS idx_conversation_messages_metadata
    ON conversation_messages USING GIN (metadata);

-- Start a session.
INSERT INTO agent_sessions (user_id, tenant_id)
VALUES (1001, 10)
RETURNING id;

-- Append the next message while preserving order.
INSERT INTO conversation_messages (
    session_id,
    sequence_no,
    role,
    content,
    token_count
)
SELECT
    1,
    COALESCE(MAX(sequence_no), 0) + 1,
    'user',
    'Summarize my recent expenses.',
    8
FROM conversation_messages
WHERE session_id = 1;

-- Read the most recent context window.
SELECT sequence_no, role, content, tool_name, created_at
FROM conversation_messages
WHERE session_id = 1
ORDER BY sequence_no DESC
LIMIT 20;

-- Persist a new summarized context version.
INSERT INTO session_context_snapshots (
    session_id,
    context_version,
    summary,
    memory
)
VALUES (
    1,
    2,
    'User is reviewing recent expenses.',
    '{"preferred_currency":"INR"}'::jsonb
);

-- Update the active session to the latest context version.
UPDATE agent_sessions
SET
    context_version = 2,
    summary = 'User is reviewing recent expenses.',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Archive an inactive session.
UPDATE agent_sessions
SET
    status = 'archived',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;
