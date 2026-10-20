# Day 81 — End-to-End System Design Exercise

**Scenario:** Design a task-management API that supports task creation, listing, updates, and completion for multiple users.

## 1. Requirements

- List functional requirements and explicitly out-of-scope features.
- Define authentication, authorization, pagination, filtering, and error behavior.
- Set measurable targets for latency, availability, and expected traffic; state assumptions.

## 2. API contract

Draft request/response examples for `POST /api/v1/tasks`, `GET /api/v1/tasks`, `GET /api/v1/tasks/{id}`, and `PATCH /api/v1/tasks/{id}`. Include validation errors, not-found behavior, and request correlation IDs.

## 3. Data model and SQL

Propose `users` and `tasks` tables, primary/foreign keys, status constraints, timestamps, and indexes justified by query patterns. Explain how ownership is enforced in every read and write.

## 4. Architecture and request flow

Trace a request through routing, authentication, validation, service logic, repository/database, and response serialization. Identify which layer owns each responsibility.

## 5. Reliability and security

Discuss transaction boundaries, duplicate requests, timeouts, retries, rate limits, secret management, input validation, logging without sensitive data, health checks, and backup/recovery.

## 6. Scale and observability

Estimate request volume and data growth. Identify likely bottlenecks, cache candidates and invalidation rules, pagination strategy, metrics, structured logs, and alerts.

## 7. Trade-offs and self-review

Compare at least one alternative architecture. Explain consistency, complexity, cost, and operational trade-offs. Finish with a five-minute verbal walkthrough and list unresolved risks.

- [ ] Requirements and assumptions are explicit.
- [ ] API behavior is consistent across success and failure cases.
- [ ] Schema and indexes match access patterns.
- [ ] Security and multi-user data isolation are addressed.
- [ ] Failure modes, observability, and recovery are covered.
