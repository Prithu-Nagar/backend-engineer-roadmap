# Day 90 — Final HLD/LLD Checklist

## Objective

Use this checklist to assess whether you can move from requirements to a defensible design, explain trade-offs, and communicate operational risks. Apply it to one familiar project rather than designing every possible component.

## High-level design (HLD)

- [ ] Clarify functional scope, users, traffic, latency, availability, and consistency requirements.
- [ ] State assumptions and estimate peak requests, storage growth, and bandwidth.
- [ ] Define APIs, data ownership, primary entities, indexes, and transaction boundaries.
- [ ] Draw the request path and justify each component.
- [ ] Identify bottlenecks and explain caching, queues, partitioning, or replication only where justified.
- [ ] Cover timeouts, bounded retries, idempotency, backpressure, and recovery.
- [ ] Address authentication, authorization, secrets, rate limiting, and abuse cases.
- [ ] Define logs, metrics, traces, alerts, health checks, and service-level indicators.
- [ ] Explain consistency, availability, cost, latency, and complexity trade-offs.

## Low-level design (LLD)

- [ ] Identify domain entities, responsibilities, and invariants.
- [ ] Keep controller, service, repository, and infrastructure responsibilities distinct where useful.
- [ ] Use interfaces and dependency injection at meaningful boundaries.
- [ ] Apply SOLID and design patterns only when they clarify change or testability.
- [ ] Define validation, error types, resource ownership, and transaction handling.
- [ ] Plan unit tests for business rules and integration tests for persistence/API behavior.
- [ ] Avoid premature abstractions and classes without clear responsibilities.

## Interview scorecard

| Dimension | Score (1–5) | Evidence / gap |
|---|---:|---|
| Requirements and estimates | | |
| API and data model | | |
| Architecture and trade-offs | | |
| Reliability and scalability | | |
| Security and observability | | |
| LLD boundaries and testability | | |
| Communication | | |

## Long-term practice

- [ ] Complete one timed HLD or LLD exercise each week.
- [ ] Review one design and write down the most important trade-off.
- [ ] Revisit weak areas using concrete feedback rather than memorized templates.
- [ ] Practice explaining a simple viable design before scaling it.

## Completion criteria

Summarize two strengths, two gaps, and a concrete next action for each gap. Do not claim production readiness without implementation, operational evidence, and tests.
