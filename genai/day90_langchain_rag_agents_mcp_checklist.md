# Day 90 — Final LangChain, RAG, Agents, and MCP Checklist

## Objective

Review the core building blocks of a GenAI-enabled backend and verify that the capstone handles retrieval, tools, evaluation, and failure modes deliberately.

## LangChain and RAG

- [ ] Explain the ingestion path: loading, cleaning, chunking, metadata, embeddings, and indexing.
- [ ] Explain similarity search, metadata filters, top-k retrieval, and the limits of vector similarity.
- [ ] Distinguish retrieval quality from answer quality; use a small representative evaluation set.
- [ ] Ground answers in retrieved context and make unsupported claims or missing context explicit.
- [ ] Track chunking choices, embedding model, prompt version, and retrieval configuration.
- [ ] Consider access control at retrieval time so users cannot retrieve documents they are not allowed to see.

## Agents and tool use

- [ ] Define the agent's permitted tools and validate each tool's input schema.
- [ ] Keep authorization and business rules in trusted application code, not model instructions.
- [ ] Set time, token, step, and cost budgets.
- [ ] Handle tool errors, timeouts, retries, and partial results safely.
- [ ] Require confirmation for consequential actions and make repeatable operations idempotent where possible.
- [ ] Separate untrusted retrieved text from trusted instructions; test prompt-injection attempts.

## Model Context Protocol (MCP)

- [ ] Explain the client/server relationship and the distinction between tools, resources, and prompts.
- [ ] Validate tool arguments and enforce authorization at the server boundary.
- [ ] Treat tool descriptions and returned content as data, not as permission to bypass policy.
- [ ] Minimize exposed capabilities and avoid leaking secrets or unrelated user data.
- [ ] Define timeout, failure, and audit behavior for external tool calls.

## Reliability, evaluation, and operations

- [ ] Test relevant, irrelevant, missing, and adversarial retrieval contexts.
- [ ] Measure retrieval quality, groundedness, task success, latency, and cost where applicable.
- [ ] Use deterministic tests for application logic and mocked model/tool responses.
- [ ] Add safe logs and request correlation without recording secrets or unnecessary personal data.
- [ ] Provide bounded retries, timeouts, fallback behavior, and a clear user-facing failure mode.
- [ ] Document model/provider assumptions, known limitations, and evaluation-set scope.

## Long-term practice

- [ ] Re-run a small evaluation set after prompt, model, embedding, or chunking changes.
- [ ] Review one failure case each week and turn it into a regression test.
- [ ] Keep a record of latency/cost trade-offs and the evidence behind model choices.

## Completion criteria

Explain the complete request flow, identify the trust boundaries, and describe how quality, safety, cost, and failure behavior are tested. Mark only features that are actually implemented.
