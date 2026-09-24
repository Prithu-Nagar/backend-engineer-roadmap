-- Day 55 — Agent / Tool Execution Logs
-- PostgreSQL-oriented schema for auditing agent runs, tool calls, and results.

CREATE TABLE agent_runs (
    run_id UUID PRIMARY KEY,
    tenant_id BIGINT,
    session_id TEXT,
    agent_name TEXT NOT NULL,
    model_name TEXT,
    status TEXT NOT NULL DEFAULT 'running',
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    CHECK (status IN ('running', 'completed', 'failed', 'cancelled'))
);

CREATE TABLE agent_tool_calls (
    tool_call_id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES agent_runs(run_id) ON DELETE CASCADE,
    tool_name TEXT NOT NULL,
    arguments JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'requested',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_code TEXT,
    CHECK (status IN ('requested', 'running', 'completed', 'failed', 'rejected'))
);

CREATE TABLE agent_tool_results (
    tool_call_id UUID PRIMARY KEY REFERENCES agent_tool_calls(tool_call_id) ON DELETE CASCADE,
    result JSONB,
    result_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_runs_session_started
    ON agent_runs (session_id, started_at DESC);

CREATE INDEX idx_agent_tool_calls_run_requested
    ON agent_tool_calls (run_id, requested_at);

CREATE INDEX idx_agent_tool_calls_tool_status
    ON agent_tool_calls (tool_name, status);

-- Example audit query: identify failed or rejected tool calls for a run.
SELECT
    c.run_id,
    c.tool_call_id,
    c.tool_name,
    c.status,
    c.error_code,
    c.requested_at,
    c.completed_at
FROM agent_tool_calls AS c
WHERE c.status IN ('failed', 'rejected')
ORDER BY c.requested_at DESC;
