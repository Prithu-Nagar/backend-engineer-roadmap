# RAG System Architecture

Day 53 focuses on the online architecture of a Retrieval-Augmented Generation
(RAG) system: query understanding, retrieval, reranking, context construction,
and generation.

---

## High-Level Flow

```text
Client
  |
  v
API / Auth
  |
  v
Query Service
  |
  +--> Query validation / normalization
  |
  v
Metadata + Tenant Filters
  |
  v
Vector / Keyword Retrieval
  |
  v
Candidate Set
  |
  v
Reranker
  |
  v
Context Construction
  |
  v
LLM
  |
  v
Answer + Sources
```

The retrieval and generation stages should remain separate so each can be
measured, replaced, and scaled independently.

## Retrieval

A retrieval service can combine:

- Vector similarity for semantic matching
- Keyword or lexical search for exact terms
- Tenant and authorization filters
- Document-type and metadata filters
- Top-K candidate limits

Security filters should be applied before context is returned to the model.

## Reranking

Initial retrieval is optimized for efficiently producing a candidate set.
A reranker can then score a smaller set using a more expensive relevance model.

```text
Large corpus
    |
    v
Fast retrieval
    |
    +--> Top 20–100 candidates
              |
              v
          Reranker
              |
              v
          Top 5–10
```

The candidate count should be large enough for recall but bounded so reranking
latency and cost remain predictable.

## Context Construction

The context builder should:

1. Remove duplicate or near-duplicate chunks.
2. Preserve source identifiers.
3. Respect token/context limits.
4. Order chunks using the selected relevance policy.
5. Add clear boundaries between sources.
6. Preserve tenant and authorization decisions from retrieval.

The model should receive only the context that the application has explicitly
selected.

## API Boundary

A production RAG API commonly separates:

- Authentication and authorization
- Query validation
- Retrieval orchestration
- Reranking
- Context construction
- LLM invocation
- Response formatting
- Observability and cost tracking

This prevents the HTTP route from becoming responsible for the entire pipeline.

## Reliability and Scaling

Key concerns include:

- Retrieval latency and timeout budgets
- Vector-store availability
- LLM provider failures
- Rate limiting
- Caching repeated queries where appropriate
- Bounded candidate and context sizes
- Async I/O for network-bound stages
- Tenant isolation
- Tracing across retrieval, reranking, and generation

## Evaluation Signals

Useful operational and quality signals include:

- Retrieval recall / hit rate
- Reranker relevance
- Empty-result rate
- End-to-end latency
- Time to first token
- Context size
- Answer quality
- Citation/source coverage
- LLM token and cost usage

## Interview Checklist

- Why separate retrieval from generation?
- Where should tenant filters be applied?
- Why use reranking after vector retrieval?
- How do you prevent context-window overflow?
- What should happen when retrieval returns no useful context?
- Which stages should be independently observable?
