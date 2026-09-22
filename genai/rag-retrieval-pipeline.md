# RAG Retrieval Pipeline

Day 53 covers the retrieval side of a Retrieval-Augmented Generation system:
chunking, candidate retrieval, reranking, and context construction.

---

## Pipeline

```text
Source Documents
      |
      v
Chunking
      |
      v
Embeddings / Search Index
      |
      v
Candidate Retrieval
      |
      v
Reranking
      |
      v
Context Construction
      |
      v
LLM Prompt
```

Each stage should have a clear input/output contract so retrieval quality and
latency can be measured independently.

## Chunking

Chunking divides source documents into retrieval units.

Important considerations:

- Chunk size
- Chunk overlap
- Sentence or section boundaries
- Metadata preservation
- Source identifiers
- Token limits

Very small chunks can lose useful context, while very large chunks can reduce
retrieval precision and consume more model context.

## Candidate Retrieval

Retrieval produces a bounded candidate set using signals such as:

- Vector similarity
- Keyword matching
- Metadata filters
- Tenant boundaries
- Document type or access constraints

Authorization and tenant filtering should be enforced before selected content
is passed to downstream model processing.

## Reranking

Reranking applies a more expensive relevance signal to a smaller candidate set.

```text
Vector / lexical retrieval
          |
          v
       Top-N
          |
          v
      Reranker
          |
          v
       Top-K
```

This two-stage approach balances broad recall with the cost of detailed
relevance scoring.

## Context Construction

The context builder should:

1. Deduplicate overlapping results.
2. Preserve source identifiers.
3. Order chunks using relevance.
4. Respect a strict token or character budget.
5. Keep source boundaries explicit.
6. Avoid adding content that was not selected by retrieval.

The context budget should be treated as a hard resource constraint rather than
an afterthought.

## Failure Cases

Handle cases such as:

- No candidates returned
- Low-confidence retrieval
- Duplicate chunks
- Oversized context
- Stale or deleted source documents
- Metadata/tenant filter mismatches
- Reranker timeouts

A production service should expose these outcomes through structured metrics
and tracing.

## Interview Questions

- How would you choose a chunk size and overlap?
- Why retrieve more candidates than the final context contains?
- What problem does reranking solve?
- Where should tenant filtering occur?
- How do you prevent context-window overflow?
- What should the system do when retrieval quality is too low?
