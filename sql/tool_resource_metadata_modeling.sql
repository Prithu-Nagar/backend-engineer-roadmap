-- Day 57 — Tool / Resource Metadata Modeling
-- PostgreSQL-oriented metadata model for MCP-style tools and resources.

CREATE TABLE mcp_servers (
    server_id UUID PRIMARY KEY,
    tenant_id BIGINT,
    server_name TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('active', 'disabled'))
);

CREATE TABLE mcp_tools (
    tool_id UUID PRIMARY KEY,
    server_id UUID NOT NULL REFERENCES mcp_servers(server_id) ON DELETE CASCADE,
    tool_name TEXT NOT NULL,
    description TEXT,
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    version TEXT,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (server_id, tool_name)
);

CREATE TABLE mcp_resources (
    resource_id UUID PRIMARY KEY,
    server_id UUID NOT NULL REFERENCES mcp_servers(server_id) ON DELETE CASCADE,
    uri TEXT NOT NULL,
    resource_name TEXT NOT NULL,
    description TEXT,
    mime_type TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (server_id, uri)
);

CREATE INDEX idx_mcp_servers_tenant_status
    ON mcp_servers (tenant_id, status);

CREATE INDEX idx_mcp_tools_server_enabled
    ON mcp_tools (server_id, enabled);

CREATE INDEX idx_mcp_resources_server_enabled
    ON mcp_resources (server_id, enabled);

-- Example: discover enabled tools exposed by an active server.
SELECT
    s.server_name,
    t.tool_name,
    t.description,
    t.input_schema,
    t.version
FROM mcp_servers AS s
JOIN mcp_tools AS t
    ON t.server_id = s.server_id
WHERE s.status = 'active'
  AND t.enabled = TRUE
ORDER BY t.tool_name;

-- Example: discover resources available to a tenant.
SELECT
    s.server_name,
    r.uri,
    r.resource_name,
    r.mime_type
FROM mcp_servers AS s
JOIN mcp_resources AS r
    ON r.server_id = s.server_id
WHERE s.tenant_id = :tenant_id
  AND s.status = 'active'
  AND r.enabled = TRUE
ORDER BY r.resource_name;
