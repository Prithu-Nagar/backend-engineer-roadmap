# Generative AI

This directory contains notes and practical examples covering Generative AI concepts relevant to backend engineering and modern AI-powered applications.

The focus is on understanding how LLM-based systems work and how they can be integrated into practical backend applications.

---

## Topics Covered

- Prompt Engineering
- Prompt Chaining
- Prompt Templates
- Tokens & Tokenization
- Embeddings
- Vector Databases
- Retrieval-Augmented Generation (RAG)
- RAG Evaluation
- Tool Integration
- LangChain Basics
- AI Agents

---

## Prompt Engineering

Covers designing effective prompts for obtaining reliable and useful model outputs.

Topics include:

- Clear instructions
- Context
- Constraints
- Output formatting
- Few-shot examples

---

## Prompt Chaining

Covers breaking complex tasks into multiple sequential LLM operations.

Topics include:

- Sequential prompts
- Intermediate outputs
- Multi-step workflows
- Structured pipelines

---

## Prompt Templates

Covers reusable prompt structures with dynamic inputs.

Topics include:

- Variables
- Reusable instructions
- Structured prompts
- Consistent model interactions

---

## Tokens & Tokenization

Covers how text is converted into tokens before being processed by an LLM.

Topics include:

- Tokens
- Tokenization
- Context windows
- Token limits
- Token usage

---

## Embeddings

Covers representing text as numerical vectors for semantic comparison.

Common applications include:

- Semantic search
- Similarity search
- Recommendation systems
- Retrieval systems

---

## Vector Databases

Covers databases designed to store and retrieve vector embeddings efficiently.

Topics include:

- Embeddings
- Similarity search
- Metadata filtering
- Approximate nearest-neighbor search

---

## Retrieval-Augmented Generation

RAG combines information retrieval with generation.

Basic flow:

text
User Query
    |
    v
Embedding
    |
    v
Vector Search
    |
    v
Relevant Context
    |
    v
LLM
    |
    v
Answer

RAG can help ground model responses in external or application-specific information.

---

## RAG Evaluation

Covers evaluating retrieval and generation quality.

Important areas include:

- Retrieval relevance
- Context quality
- Answer correctness
- Faithfulness
- Groundedness
- End-to-end evaluation

---

## Tool Integration

Tool integration allows an LLM application to interact with controlled external systems and backend functions.

Examples include:

- Database lookups
- API calls
- Application services
- Calculations
- Resource operations

The application should control tool execution and validate the model-generated arguments.

File: `tool_integration.md`

### Basic Flow

text
User
 |
 v
LLM
 |
 | Tool Call
 v
Application
 |
 v
Tool
 |
 v
Tool Result
 |
 v
LLM
 |
 v
Final Response

Tool calling and RAG can also be combined when an application needs both retrieved knowledge and live application data.

---

## AI Agents — Day 19

Day 19 introduces AI agent fundamentals.

Topics include:

- AI agents
- Agent architecture
- Tool calling
- Tool schemas
- Agent loops
- Agent state
- Stopping conditions
- Tool validation
- Guardrails
- Agent reliability
- Agents vs RAG

File:

`agents.md`

A key principle is that the LLM can select an action, but the
application remains responsible for validating and executing that action.

The backend should control:

- Authorization
- Tool validation
- Tool execution
- State
- Rate limits
- Error handling

---

## Repository Structure

genai/
├── README.md
├── agents.md
├── embeddings.md
├── langchain_basics.md
├── prompt_chaining.md
├── prompt_templates.md
├── rag.md
├── rag_evaluation.md
├── tokens_and_tokenization.md
├── tool_integration.md
└── vector_databases.md

---

## Completed Topics

- Prompt Engineering
- Prompt Chaining
- Prompt Templates
- Tokens & Tokenization
- Embeddings
- Vector Databases
- Retrieval-Augmented Generation
- RAG Evaluation
- Tool Integration

---

## Upcoming Topics

- AI Agents
- Model Context Protocol (MCP)

---

## Learning Approach

For each Generative AI topic:

1. Understand the underlying concept.
2. Understand where it fits in an AI application.
3. Implement or document a practical example.
4. Understand limitations and failure modes.
5. Consider security and reliability.
6. Apply the concept to backend and AI-powered projects.

