# RAG / Agent Prototype

A provider-neutral RAG/Agent backend prototype with document ingestion, chunking, metadata-aware embeddings, vector retrieval, grounded answer generation, source references, and a bounded application-owned tool boundary.

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
                              Bounded Context
                                      |
                                      v
                         Grounded Answer Generator
                                      |
                         Citation / Abstention Check

Agent Requests --> Allow-listed Tool Registry --> One approved tool call
```

## Components

- `rag_agent.py` retains `DocumentChunk`, the deterministic `LexicalRetriever`, the allow-listed `ToolRegistry`, and `RagAgent`. Tool names are allow-listed, required arguments are validated and length-bounded, and one deterministic tool route is executed per request.
- `rag_ingestion.py` provides UTF-8 text/Markdown loading, metadata-aware chunking, an `EmbeddingProvider` interface, live OpenAI embeddings, deterministic local feature hashing, an in-memory vector store, and vector retrieval.
- `rag_generation.py` provides a provider-neutral answer stage, a live OpenAI Chat Completions adapter, bounded source/context selection, citation allow-list validation, and explicit abstention when evidence is missing or citations are invalid.
- `rag_evaluation.py` calculates deterministic Precision@K, Recall@K, and MRR over the versioned `evaluation_cases.json` regression set.
- `demo.py` demonstrates ingestion and retrieval offline, or live retrieval and grounded generation with `--live`.
- Chunk metadata retains caller-supplied source fields plus `chunk_index`, `start_char`, and `end_char`.

## Setup and configuration

The implementation uses the Python standard library at runtime. Install the test dependency in your environment:

```bash
python -m pip install pytest
```

Set `OPENAI_API_KEY` only when using live provider integrations. Optional model overrides are:

| Variable | Default | Used by |
| --- | --- | --- |
| `OPENAI_CHAT_MODEL` | `gpt-4o-mini` | Live answer generation |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Live embeddings |

The adapters also accept explicit model names and positive request timeouts in their constructors. Never commit API keys.

## Run the demo

From the repository root:

```bash
python projects/rag-agent-prototype/demo.py
```

This runs local feature-hashing retrieval and clearly labels that mode as offline; it does not pretend to generate a live answer. For live embeddings and grounded answer generation:

```bash
python projects/rag-agent-prototype/demo.py --live
```

The live mode requires `OPENAI_API_KEY` and can incur provider charges. Use a short question and a small document set when experimenting.

## Evaluation and tests

Run all RAG tests, including the generation test module retained at the project root:

```bash
python -m pytest projects/rag-agent-prototype -q
```

Run the deterministic retrieval evaluation set:

```bash
PYTHONPATH=projects/rag-agent-prototype python -c "from pathlib import Path; from rag_agent import DocumentChunk, LexicalRetriever; from rag_evaluation import load_evaluation_cases, evaluate_retrieval; r=LexicalRetriever([DocumentChunk('backend-rate-limits', 'AI endpoints use tenant-aware rate limits and token budgets to control cost.'), DocumentChunk('rag-retrieval', 'RAG separates document ingestion, chunking, retrieval, context assembly, and answer generation.'), DocumentChunk('ai-reliability', 'AI services use bounded retries, timeouts, fallbacks, and stable client-facing errors.')]); print(evaluate_retrieval(r, load_evaluation_cases(Path('projects/rag-agent-prototype/evaluation_cases.json')), top_k=2))"
```

The tests cover ingestion, chunk metadata, empty input, embedding and vector-store validation, provider response parsing and failures, grounded citations, invalid/unknown citations, abstention, context/source bounds, tool allow-listing and argument limits, and compatibility with the original lexical agent.

## Provider boundaries and cost

- `OpenAIEmbeddingProvider` and `OpenAIChatCompletionProvider` make real remote API requests when explicitly instantiated with credentials.
- `HashingEmbeddingProvider` is a deterministic local feature-hashing fallback for offline demonstrations and tests. It is **not** a semantic embedding model.
- `FakeProvider` in tests is a test double; it does not call a model. The offline demo skips answer generation rather than substituting a fake answer.
- Provider calls are not made by the automated test suite. Live API behavior is exercised only when a user explicitly runs the `--live` demo with credentials.

Estimate variable provider cost using the provider's current published rates:

```text
embedding cost = embedding input tokens / 1,000,000 × embedding input rate
generation cost = (prompt input tokens × input rate
                 + generated output tokens × output rate) / 1,000,000
total estimated cost = embedding cost + generation cost
```

Actual usage depends on document volume, chunk overlap, model choice, prompt/context size, question volume, and generated output length. This prototype does not currently record token usage, latency, or monetary cost, so it must not report measured cost or performance figures.

## Limitations and safety boundaries

- The vector store is in-memory only; indexed records are lost when the process exits.
- The local hashing embedder is deterministic but not semantic. Retrieval quality from that mode is only a demonstration baseline.
- Citation validation checks that cited source identifiers were among the selected retrieved sources. It does not prove that every sentence is entailed by its cited text; semantic faithfulness still needs human or model-based evaluation.
- Retrieved source text is treated as untrusted data in the live generation instruction, but prompt injection cannot be eliminated by prompting alone.
- Tool execution is deterministic and application-owned, not an unrestricted model tool loop. Only registered tools can run; the current agent performs at most one approved tool call per request and bounds the required argument.
- Persistent vector databases, tenant isolation, document-format loaders, token/latency telemetry, and production-scale indexing are outside this MVP.

## Original agent compatibility

`rag_agent.py` remains directly runnable for its original lexical retrieval and demo service-status tool example:

```bash
python projects/rag-agent-prototype/rag_agent.py
```
