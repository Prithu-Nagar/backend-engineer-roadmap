-- Day 51 — RAG Metadata / Query Patterns
-- PostgreSQL-oriented examples for storing and filtering document metadata.
--
-- The examples separate document identity, chunk content, and retrieval
-- metadata so retrieval queries can apply business filters before ranking.

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL,
    chunk_text TEXT NOT NULL,
    source_uri TEXT NOT NULL,
    tenant_id BIGINT NOT NULL,
    document_type TEXT NOT NULL,
    language_code TEXT NOT NULL DEFAULT 'en',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_document_chunks_tenant_type
    ON document_chunks (tenant_id, document_type);

CREATE INDEX IF NOT EXISTS idx_document_chunks_metadata
    ON document_chunks USING GIN (metadata);

-- Retrieve candidate chunks for a tenant and document type.
SELECT chunk_id, document_id, chunk_text, source_uri, metadata
FROM document_chunks
WHERE tenant_id = $1
  AND document_type = $2
ORDER BY created_at DESC
LIMIT $3;

-- Filter by a metadata attribute before passing candidates to a vector
-- similarity layer.
SELECT chunk_id, document_id, chunk_text
FROM document_chunks
WHERE tenant_id = $1
  AND metadata @> jsonb_build_object('product', $2)
ORDER BY created_at DESC
LIMIT $3;

-- Combine multiple metadata constraints while keeping parameters bound.
SELECT chunk_id, document_id, chunk_text
FROM document_chunks
WHERE tenant_id = $1
  AND document_type = ANY($2)
  AND language_code = $3
  AND metadata @> $4::jsonb
ORDER BY created_at DESC
LIMIT $5;

-- Count chunks by source to support ingestion-quality checks.
SELECT source_uri, COUNT(*) AS chunk_count
FROM document_chunks
WHERE tenant_id = $1
GROUP BY source_uri
ORDER BY chunk_count DESC;
