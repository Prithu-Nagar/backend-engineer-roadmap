# Generative AI

This directory contains practical notes and examples covering Generative AI, Large Language Models, embeddings, vector databases, and Retrieval-Augmented Generation.

The focus is on understanding the core concepts behind modern LLM-powered applications and how they can be applied to backend systems.

---

# Topics

## Prompt Engineering

Covers techniques for designing effective prompts for Large Language Models.

Topics include:

- Clear instructions
- Context
- Constraints
- Output formatting
- Few-shot examples

---

## Prompt Chaining

Covers breaking complex tasks into multiple sequential LLM calls.

Topics include:

- Sequential prompts
- Intermediate outputs
- Multi-step workflows
- Chaining LLM operations

File: `prompt_chaining.md`

---

## Prompt Templates

Covers reusable prompt structures that can be populated with dynamic inputs.

Topics include:

- Template variables
- Reusable prompts
- Structured prompt construction

File: `prompt_templates.md`

---

## Tokens & Tokenization

Covers how text is converted into tokens before being processed by an LLM.

Topics include:

- Tokens
- Tokenization
- Token limits
- Context windows
- Token usage

File: `tokens_and_tokenization.md`

---

## Embeddings

Covers converting text into numerical vector representations that capture semantic relationships.

Topics include:

- Embedding vectors
- Semantic similarity
- Vector representations
- Similarity search

File: `embeddings.md`

---

## Vector Databases

Covers storing and searching vector embeddings.

Topics include:

- Vector storage
- Similarity search
- Nearest-neighbor search
- Metadata filtering
- Vector database use cases

File: `vector_databases.md`

---

## Retrieval-Augmented Generation (RAG)

Covers combining information retrieval with Large Language Models.

A typical RAG pipeline is:

User Query
    ↓
Query Processing
    ↓
Embedding
    ↓
Vector Search
    ↓
Relevant Documents
    ↓
Context
    ↓
LLM
    ↓
Generated Answer

File: `rag.md`

---

## RAG Evaluation

Covers evaluating the quality of both retrieval and generated responses in a RAG system.

Topics include:

- Precision
- Recall
- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)
- NDCG
- Faithfulness
- Answer Relevance
- Correctness
- Retrieval vs generation failures

File: `rag_evaluation.md`

---

# Repository Structure

genai/
├── README.md
├── prompt_chaining.md
├── prompt_templates.md
├── tokens_and_tokenization.md
├── embeddings.md
├── vector_databases.md
├── rag.md
└── rag_evaluation.md

---

# Completed Topics

- Prompt Engineering
- Prompt Chaining
- Prompt Templates
- Tokens & Tokenization
- Embeddings
- Vector Databases
- Retrieval-Augmented Generation (RAG)
- RAG Evaluation

---

# Upcoming Topics

- LangChain
- AI Agents
- Vector Search
- Model Context Protocol (MCP)
- Advanced RAG
- LLM Application Architecture

---

# Learning Approach

For each Generative AI topic:

1. Understand the underlying concept.
2. Study how it is used in LLM-powered applications.
3. Implement or analyze practical examples where appropriate.
4. Understand the limitations and trade-offs.
5. Connect the concept to backend and production use cases.
