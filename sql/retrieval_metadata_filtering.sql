-- Day 53 — Metadata Filtering for Retrieval
-- PostgreSQL-oriented patterns for narrowing RAG candidates before ranking.

-- Filter candidates by tenant, source type, language, and JSONB metadata.
SELECT
    chunk_id,
    document_id,
    chunk_text,
    metadata
FROM document_chunks
WHERE tenant_id = $1
  AND document_type = ANY($2)
  AND language_code = $3
  AND metadata @> $4::jsonb
ORDER BY created_at DESC
LIMIT $5;

-- Build a filtered candidate set before applying vector similarity.
WITH candidates AS (
    SELECT
        chunk_id,
        document_id,
        chunk_text,
        metadata,
        embedding
    FROM document_chunks
    WHERE tenant_id = $1
      AND metadata @> $2::jsonb
)
SELECT
    chunk_id,
    document_id,
    chunk_text,
    metadata,
    1 - (embedding <=> $3::vector) AS similarity
FROM candidates
WHERE embedding IS NOT NULL
ORDER BY embedding <=> $3::vector
LIMIT $4;

-- Filter by nested JSONB attributes.
SELECT chunk_id, document_id, chunk_text
FROM document_chunks
WHERE tenant_id = $1
  AND metadata -> 'access' ->> 'visibility' = $2
  AND metadata ->> 'product' = $3
ORDER BY created_at DESC
LIMIT $4;

-- Keep metadata filtering parameterized; do not concatenate user input into SQL.
-- The application should validate allowed filter fields and values before binding
-- parameters to the query.
