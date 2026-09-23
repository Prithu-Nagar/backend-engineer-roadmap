# Offline Ingestion vs Online Serving

Day 54 separates the RAG ingestion pipeline from the latency-sensitive online
query path. Documents can be processed, chunked, embedded, validated, and
indexed ahead of time so serving requests only perform retrieval, context
construction, and generation.

---

## High-Level Architecture

```text
                    OFFLINE / ASYNCHRONOUS
Source Files
    |
    v
Ingestion Job
    |
    v
Parsing / Cleaning
    |
    v
Chunking
    |
    v
Embedding Generation
    |
    v
Validation + Metadata
    |
    v
Vector / Metadata Store

                    ONLINE / SYNCHRONOUS
Client
  |
  v
RAG API
  |
  v
Query Validation
  |
  v
Retrieval + Metadata Filters
  |
  v
Reranking / Context Construction
  |
  v
LLM
  |
  v
Answer + Sources
```

The two paths share the indexed data contract but have different latency and
reliability requirements.

## Offline Ingestion

Offline work can include:

- File ingestion and parsing
- Text normalization
- Chunking and overlap management
- Metadata extraction
- Embedding generation
- Duplicate detection
- Validation and quality checks
- Index updates
- Retry and dead-letter handling

These tasks can run asynchronously because they do not need to block an end
user's query.

## Online Serving

The online path should remain bounded and predictable.

Typical stages are:

1. Authenticate and authorize the caller.
2. Validate and normalize the query.
3. Apply tenant and metadata filters.
4. Retrieve candidate chunks.
5. Rerank candidates when required.
6. Construct bounded context.
7. Call the LLM.
8. Return the answer and source references.

The online path should not parse large source files or generate embeddings for
an entire corpus during a user request.

## Queue-Based Ingestion

A queue provides a durable boundary between upload events and processing.

```text
Upload Event
     |
     v
Job Queue
     |
     +----> Worker 1 ----> Parse / Chunk
     |
     +----> Worker 2 ----> Embed / Index
     |
     +----> Worker N ----> Validate / Retry
```

Useful job properties include:

- Stable job ID
- Tenant ID
- Source document ID
- Idempotency key
- Attempt count
- Status
- Error information
- Created and completed timestamps

## Consistency and Versioning

Ingestion should make document versions explicit. A serving request should not
mix chunks from incompatible document or embedding versions.

Useful fields include:

- `document_version`
- `embedding_model`
- `embedding_dimension`
- `chunking_version`
- `ingestion_status`

When an index is rebuilt, the new version can be validated before it becomes
the active serving version.

## Failure Handling

Offline failures should be isolated from the online query path.

Examples:

- Parser failure → mark the ingestion job failed.
- Embedding provider timeout → retry with bounded backoff.
- Invalid metadata → reject or quarantine the document.
- Index write failure → retry without acknowledging the job.
- Repeated failure → move the job to a dead-letter workflow.

Online serving should be able to continue using the last known-good indexed
version while ingestion repairs are in progress.

## Scaling

Offline and online workloads scale independently.

| Concern | Offline ingestion | Online serving |
| --- | --- | --- |
| Primary goal | Throughput | Low latency |
| Workload | Batch / asynchronous | Request-driven |
| Scaling unit | Workers | API instances / retrieval capacity |
| Failure strategy | Retry / dead letter | Timeout / fallback |
| Resource focus | CPU, embedding throughput, storage writes | Latency, concurrency, model capacity |
| Deployment | Job workers | Stateless API services |

## Interview Checklist

- Why should ingestion be separated from online serving?
- What belongs in an ingestion job record?
- How would you make ingestion idempotent?
- How do document and embedding versions prevent inconsistent indexes?
- What happens when an embedding provider is unavailable?
- How can the system keep serving while an index is rebuilt?
