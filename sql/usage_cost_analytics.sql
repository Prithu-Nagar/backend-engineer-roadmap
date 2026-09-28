-- Day 59 — Usage / Cost Analytics
-- PostgreSQL-oriented schema for tracking AI API usage, latency, and cost.

CREATE TABLE ai_usage_events (
    usage_id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    request_id TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    latency_ms INTEGER NOT NULL,
    estimated_cost NUMERIC(14, 8) NOT NULL DEFAULT 0,
    cache_hit BOOLEAN NOT NULL DEFAULT FALSE,
    CHECK (status IN ('success', 'rate_limited', 'timeout', 'provider_error')),
    CHECK (input_tokens >= 0),
    CHECK (output_tokens >= 0),
    CHECK (latency_ms >= 0),
    CHECK (estimated_cost >= 0),
    UNIQUE (tenant_id, request_id)
);

CREATE INDEX idx_ai_usage_tenant_time
    ON ai_usage_events (tenant_id, requested_at);

CREATE INDEX idx_ai_usage_model_time
    ON ai_usage_events (model_name, requested_at);

CREATE INDEX idx_ai_usage_endpoint_status
    ON ai_usage_events (endpoint, status);

-- Daily usage and cost by model.
SELECT
    DATE_TRUNC('day', requested_at) AS usage_day,
    model_name,
    COUNT(*) AS request_count,
    SUM(input_tokens) AS input_tokens,
    SUM(output_tokens) AS output_tokens,
    SUM(estimated_cost) AS estimated_cost,
    AVG(latency_ms) AS average_latency_ms,
    AVG(CASE WHEN cache_hit THEN 1.0 ELSE 0.0 END) AS cache_hit_rate
FROM ai_usage_events
WHERE status = 'success'
GROUP BY DATE_TRUNC('day', requested_at), model_name
ORDER BY usage_day, model_name;

-- Tenant-level cost concentration for the selected period.
SELECT
    tenant_id,
    COUNT(*) AS successful_requests,
    SUM(input_tokens + output_tokens) AS total_tokens,
    SUM(estimated_cost) AS estimated_cost
FROM ai_usage_events
WHERE status = 'success'
  AND requested_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY tenant_id
ORDER BY estimated_cost DESC;

-- Endpoint latency and failure profile.
SELECT
    endpoint,
    COUNT(*) AS total_requests,
    AVG(latency_ms) FILTER (WHERE status = 'success') AS average_success_latency_ms,
    COUNT(*) FILTER (WHERE status = 'rate_limited') AS rate_limited_requests,
    COUNT(*) FILTER (WHERE status = 'timeout') AS timeout_requests,
    COUNT(*) FILTER (WHERE status = 'provider_error') AS provider_errors
FROM ai_usage_events
GROUP BY endpoint
ORDER BY endpoint;
