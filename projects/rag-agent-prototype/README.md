# RAG / Agent Prototype

A provider-neutral RAG/Agent backend prototype with document ingestion, metadata-aware chunking, embedding generation, vector retrieval, and an application-owned tool boundary.

## Architecture

```text
Source Documents
      |
      v
Document Ingestion --> Chunking + Metadata
                              |
                              v
                       Embedding Provider
                              |
                              v
                       Vector Store
                              |
User Query --> Query Embedding --> Vector Retriever
                                      |
                                      v
                              Ranked Context
                                      |
                                      v
                              Agent Boundary
                                      |
                         Approved Tool Registry
```

## Components

- `rag_agent.py` retains the original `DocumentChunk`, deterministic `LexicalRetriever`, allow-listed `ToolRegistry`, and `RagAgent` routing behavior. Chunk metadata is additive and optional, preserving existing callers.
- `rag_generation.py` provides a provider-neutral grounded-answer stage, a live OpenAI Chat Completions adapter, bounded source/context selection, citation validation, and explicit abstention when evidence is missing or citations are invalid.\n- `rag_ingestion.py` provides `load_text_file` for UTF-8 text/Markdown input, `SourceDocument`, `DocumentChunker`, `DocumentIngestionPipeline`, an `EmbeddingProvider` interface, `OpenAIEmbeddingProvider`, `HashingEmbeddingProvider`, `InMemoryVectorStore`, and `VectorRetriever`.
- Chunk metadata carries caller-supplied source fields plus `chunk_index`, `start_char`, and `end_char` offsets.
- The vector store ranks records by cosine similarity and validates vector dimensions. It is in-memory only; records are not persisted across process restarts.

## Embeddings and configuration

For live embeddings, set `OPENAI_API_KEY` in the environment and instantiate `OpenAIEmbeddingProvider`. The default model is `text-embedding-3-small`; callers may supply another compatible model. Provider errors are surfaced rather than silently replaced with local vectors.

`HashingEmbeddingProvider` is a deterministic, dependency-free feature-hashing implementation for offline tests and local demonstrations. It is **not** a semantic embedding model and must not be represented as a live embedding integration.

The prototype uses an in-memory cosine-similarity store. A persistent vector database, batching limits for large corpora, document-format loaders, tenant isolation, and production-scale indexing remain future work.

## Run

From the repository root:

```bash
python projects/rag-agent-prototype/rag_agent.py
```

## Test

From the repository root:

```bash
PYTHONPATH=projects/rag-agent-prototype pytest projects/rag-agent-prototype/tests -q
```

The tests cover grounded answers, citation validation, abstention, bounded context/source selection, chunk boundaries and metadata, empty input, embedding behavior, vector-store validation and ranking, the provider response adapter, and compatibility with the original lexical retriever and agent flow. The live embedding and chat-completion endpoints are not called by the test suite. Configure `OPENAI_API_KEY` and instantiate `OpenAIChatCompletionProvider` for live answer generation; tests use a deterministic fake provider.

## Agent and retrieval boundary

The existing agent continues to route supported status requests through an allow-listed tool registry. Retrieval context is returned with document identifiers and an explicit answer boundary; this prototype does not claim to implement live LLM answer generation or unrestricted tool execution.
