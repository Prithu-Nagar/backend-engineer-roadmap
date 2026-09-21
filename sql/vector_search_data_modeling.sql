-- Day 52 — Vector Search Data Modeling
-- PostgreSQL-oriented schema for document chunks, embeddings, and retrieval metadata.
-- Requires the pgvector extension when the vector column/index are used.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    source_uri TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, external_id)
);

CREATE TABLE document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX documents_tenant_idx
    ON documents (tenant_id);

CREATE INDEX document_chunks_document_idx
    ON document_chunks (document_id, chunk_index);

CREATE INDEX document_chunks_metadata_gin_idx
    ON document_chunks USING GIN (metadata);

-- HNSW supports approximate nearest-neighbor retrieval for cosine distance.
CREATE INDEX document_chunks_embedding_hnsw_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- Tenant-aware retrieval should filter by tenant before returning context.
-- Example shape; replace the placeholder vector with a parameter from the application.
-- SELECT id, document_id, content, metadata,
--        1 - (embedding <=> $1::vector) AS similarity
-- FROM document_chunks
-- WHERE document_id IN (
--     SELECT id FROM documents WHERE tenant_id = $2
-- )
-- ORDER BY embedding <=> $1::vector
-- LIMIT $3;
