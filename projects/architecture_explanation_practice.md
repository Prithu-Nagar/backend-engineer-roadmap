# Architecture Explanation Practice

Use this worksheet to explain a portfolio project clearly in an interview. Replace prompts with details that are true of the implementation; do not claim technologies, scale, or results that you have not built or measured.

## 1. One-Minute Overview

- **Problem:** What user or business problem does the project solve?
- **Users:** Who uses it, and what are their main workflows?
- **Core capabilities:** Name the three most important behaviors.
- **Constraints:** State the key reliability, security, latency, or cost constraints.
- **Outcome:** Describe implemented behavior and verified evidence.

## 2. Architecture Walkthrough

Explain the request path in order:

1. Client and API entry point.
2. Authentication and authorization.
3. Validation and business logic.
4. Persistence and transaction boundary.
5. Cache, queue, or external dependency, if actually present.
6. Response, error handling, and observability.

For every component, answer: why is it present, what responsibility does it own, and what would fail if it were removed?

## 3. Data and API Design

- Identify the main entities and their relationships.
- Explain primary keys, foreign keys, uniqueness rules, and important indexes.
- Describe one API endpoint, including request validation and success/error responses.
- Explain pagination, idempotency, and versioning where relevant.
- Identify the source of truth and how migrations are applied.

## 4. Failure Scenarios

Choose at least three and walk through detection, containment, recovery, and verification:

- Database unavailable or slow.
- External service timeout.
- Duplicate request or message.
- Invalid input or unauthorized access.
- Partial deployment or incompatible schema change.
- Queue backlog or worker crash.

Distinguish what the current project handles from improvements you would make next.

## 5. Security and Operations

Discuss secrets management, least privilege, input validation, sensitive-data logging, rate limiting, dependency updates, health checks, structured logs, metrics, tracing, backups, and restore testing. Mention only controls that are implemented as implemented.

## 6. Trade-Offs and Alternatives

Prepare one decision for each category that applies:
- Relational schema versus a different storage model.
- Synchronous call versus asynchronous processing.
- Cache versus direct database access.
- Simpler architecture versus additional services.
- Consistency, latency, availability, and operating cost.

State the rejected alternative and the condition that would make you reconsider.

## 7. Evidence and Follow-Up Work

- Link to relevant source files and tests.
- Demonstrate one successful flow and one failure path.
- Show test and lint results where available.
- Record known limitations honestly.
- List the next three improvements in priority order.

## 8. Two-Minute Practice Rubric

Score each item from 0 (missing) to 2 (clear and evidence-based):
- Problem and requirements.
- Request/data flow.
- Data model and API contract.
- Failure handling.
- Security and observability.
- Trade-offs and limitations.

A strong explanation is specific, structured, and honest about what has and has not been implemented.
