# RAG / Agent Prototype

Day 60 closes the GenAI Engineering phase with a small provider-neutral
prototype that combines retrieval with an application-owned tool boundary.

## Goal

Demonstrate the core flow of a RAG/Agent backend without requiring an external
LLM provider, API key, hosted vector database, or network connection.

## Architecture

```text
User Query
    |
    v
Agent Router
    |
    +----> Retriever ----> Ranked Context
    |                         |
    |                         v
    |                    Answer Boundary
    |
    +----> Tool Registry ---> Validated Tool ---> Tool Result
```

## Components

### `rag_agent.py`

The prototype contains four small application-owned boundaries:

- `DocumentChunk` — normalized retrieval unit
- `LexicalRetriever` — deterministic top-k retrieval implementation
- `ToolRegistry` — allow-listed tool execution with argument validation
- `RagAgent` — routing between retrieval and an approved tool

The lexical retriever intentionally stands in for a vector-search component so
the learning example remains deterministic and dependency-free.

## RAG Flow

1. Documents are represented as normalized chunks.
2. A query is tokenized and matched against chunk tokens.
3. Matching chunks are ranked by overlap score.
4. The top results are assembled into an explicit context boundary.
5. A production implementation could pass that context to an LLM answer step.

## Agent Flow

1. The application receives a user query.
2. The router recognizes the supported tool-intent shape.
3. The tool registry checks that the requested tool is allow-listed.
4. Required arguments are validated before execution.
5. The tool result is returned through the application boundary.

The example does not allow arbitrary function names or arbitrary internal
resource access.

## Run

From the repository root:

```bash
python projects/rag-agent-prototype/rag_agent.py
```

The script prints one retrieval example and one approved-tool example.

## Production Evolution

A production version could replace the deterministic components with:

- Embedding generation
- A vector database or pgvector
- An LLM provider behind an application-owned interface
- Structured model/tool calls
- Persistent conversation state
- Authentication and tenant authorization
- Rate limits and token budgets
- Tracing, metrics, cost tracking, and evaluation

Those additions are intentionally outside this Day 60 learning prototype.

## Day 60 Review Connection

The prototype ties together the phase's earlier work on RAG retrieval, agent
tool boundaries, AI backend validation, rate limiting, reliability, and cost
observability without replacing the dedicated learning examples in the rest of
the repository.
