-- Day 54 — RAG Evaluation Dataset Storage
-- PostgreSQL-oriented schema for storing reproducible RAG evaluation cases,
-- expected sources, and evaluation runs.

CREATE TABLE rag_evaluation_cases (
    case_id BIGSERIAL PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    dataset_version TEXT NOT NULL,
    tenant_id BIGINT,
    question TEXT NOT NULL,
    expected_answer TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (dataset_name, dataset_version, case_id)
);

CREATE TABLE rag_evaluation_case_sources (
    case_id BIGINT NOT NULL REFERENCES rag_evaluation_cases(case_id) ON DELETE CASCADE,
    document_id TEXT NOT NULL,
    chunk_id TEXT,
    relevance_grade SMALLINT,
    PRIMARY KEY (case_id, document_id, chunk_id),
    CHECK (relevance_grade IS NULL OR relevance_grade BETWEEN 0 AND 3)
);

CREATE TABLE rag_evaluation_runs (
    run_id BIGSERIAL PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    dataset_version TEXT NOT NULL,
    pipeline_version TEXT NOT NULL,
    model_name TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

CREATE TABLE rag_evaluation_results (
    result_id BIGSERIAL PRIMARY KEY,
    run_id BIGINT NOT NULL REFERENCES rag_evaluation_runs(run_id) ON DELETE CASCADE,
    case_id BIGINT NOT NULL REFERENCES rag_evaluation_cases(case_id) ON DELETE CASCADE,
    retrieval_precision_at_k NUMERIC,
    retrieval_recall_at_k NUMERIC,
    reciprocal_rank NUMERIC,
    answer_faithfulness NUMERIC,
    answer_relevance NUMERIC,
    answer_correctness NUMERIC,
    latency_ms INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    passed BOOLEAN,
    error_message TEXT,
    UNIQUE (run_id, case_id)
);

CREATE INDEX idx_rag_eval_cases_dataset
    ON rag_evaluation_cases (dataset_name, dataset_version);

CREATE INDEX idx_rag_eval_results_run
    ON rag_evaluation_results (run_id);

CREATE INDEX idx_rag_eval_cases_metadata
    ON rag_evaluation_cases USING GIN (metadata);

-- Reproducible test-set selection.
SELECT
    c.case_id,
    c.question,
    c.expected_answer,
    c.metadata
FROM rag_evaluation_cases AS c
WHERE c.dataset_name = $1
  AND c.dataset_version = $2
ORDER BY c.case_id;

-- Compare average quality and latency for one evaluation run.
SELECT
    AVG(retrieval_precision_at_k) AS avg_precision_at_k,
    AVG(retrieval_recall_at_k) AS avg_recall_at_k,
    AVG(answer_faithfulness) AS avg_faithfulness,
    AVG(answer_relevance) AS avg_relevance,
    AVG(answer_correctness) AS avg_correctness,
    AVG(latency_ms) AS avg_latency_ms
FROM rag_evaluation_results
WHERE run_id = $1;

-- Store raw evaluator output separately if needed; keep this result table
-- focused on stable metrics that can be compared across pipeline versions.
