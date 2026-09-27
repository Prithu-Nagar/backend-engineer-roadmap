-- Day 58 — Evaluation Result Storage
-- PostgreSQL-oriented schema for storing reproducible AI evaluation results.

CREATE TABLE evaluation_datasets (
    dataset_id UUID PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    version TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (dataset_name, version)
);

CREATE TABLE evaluation_cases (
    case_id UUID PRIMARY KEY,
    dataset_id UUID NOT NULL REFERENCES evaluation_datasets(dataset_id)
        ON DELETE CASCADE,
    case_key TEXT NOT NULL,
    input_text TEXT NOT NULL,
    expected_output TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (dataset_id, case_key)
);

CREATE TABLE evaluation_runs (
    run_id UUID PRIMARY KEY,
    dataset_id UUID NOT NULL REFERENCES evaluation_datasets(dataset_id),
    pipeline_version TEXT NOT NULL,
    model_name TEXT NOT NULL,
    prompt_version TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'running',
    CHECK (status IN ('running', 'completed', 'failed'))
);

CREATE TABLE evaluation_results (
    result_id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES evaluation_runs(run_id)
        ON DELETE CASCADE,
    case_id UUID NOT NULL REFERENCES evaluation_cases(case_id)
        ON DELETE CASCADE,
    output_text TEXT,
    retrieval_score NUMERIC,
    answer_score NUMERIC,
    latency_ms INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    passed BOOLEAN,
    error_code TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (run_id, case_id)
);

CREATE INDEX idx_evaluation_cases_dataset
    ON evaluation_cases (dataset_id);

CREATE INDEX idx_evaluation_runs_dataset_status
    ON evaluation_runs (dataset_id, status);

CREATE INDEX idx_evaluation_results_run_passed
    ON evaluation_results (run_id, passed);

-- Compare pass rates and average latency for a completed evaluation run.
SELECT
    r.run_id,
    r.model_name,
    r.pipeline_version,
    AVG(CASE WHEN er.passed THEN 1.0 ELSE 0.0 END) AS pass_rate,
    AVG(er.latency_ms) AS average_latency_ms,
    AVG(er.input_tokens + er.output_tokens) AS average_total_tokens
FROM evaluation_runs AS r
JOIN evaluation_results AS er
    ON er.run_id = r.run_id
WHERE r.status = 'completed'
GROUP BY r.run_id, r.model_name, r.pipeline_version
ORDER BY r.run_id;
