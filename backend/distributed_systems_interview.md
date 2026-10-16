# Distributed Systems — Backend Interview Questions

Use these prompts to structure answers around failure modes, consistency, delivery semantics, and operational trade-offs rather than naming technologies without explaining why they fit.

## 1. What makes a system distributed?

Multiple independent processes or machines coordinate over a network. Network latency, partial failures, duplicated messages, clock differences, and independent deployments mean the system cannot assume one shared memory space or one perfectly reliable process.

## 2. What is the difference between availability and consistency?

Explain the actual product requirement first. In a partition scenario, a design may have to choose whether to reject or delay some operations to preserve a stronger consistency guarantee, or accept operations that can temporarily diverge. Avoid presenting CAP as a general choice between any two properties at all times.

## 3. How do you make event processing idempotent?

Give each event a stable identifier. Record processed identifiers or use a business-level uniqueness constraint in the same transaction as the side effect where possible. For external side effects, use an idempotency key or an outbox/inbox workflow and define retention for deduplication records.

## 4. What is the difference between at-most-once, at-least-once, and effectively-once processing?

- **At-most-once:** a message is not retried after certain failures, so loss is possible.
- **At-least-once:** retries improve delivery but duplicates are possible.
- **Effectively-once business effect:** duplicates are controlled through idempotency, transactional boundaries, and carefully designed side effects. Do not claim that transport alone guarantees exactly-once behavior across arbitrary external systems.

## 5. How would you prevent a database update and event publish from diverging?

Describe the dual-write problem. A transactional outbox stores the state change and event record in one database transaction; a publisher relays pending records and marks progress. Consumers remain idempotent because relay delivery can repeat.

## 6. How do you handle retries?

Use bounded retries, exponential backoff, jitter, timeouts, and an overall deadline. Classify retryable and non-retryable errors. Consider circuit breaking and load shedding, and route poison messages to a dead-letter or quarantine workflow with a replay process.

## 7. How do you reason about ordering?

Define the scope of ordering required. Partition by a key that represents the ordering boundary, attach sequence/version information where needed, and make consumers detect stale or out-of-order updates. Global ordering often reduces throughput and availability.

## 8. What is a saga?

A saga coordinates a multi-step business workflow through local transactions and compensating actions. Compensation is not always a literal rollback; it may be a new business action. Explain timeout handling, duplicate commands, observability, and manual repair paths.

## 9. How do you investigate rising latency across services?

- Compare p50, p95, and p99 latency with traffic and error rate.
- Trace a representative slow request across service boundaries.
- Inspect queue depth, saturation, dependency latency, connection pools, and retry volume.
- Correlate the start of the regression with deployments and configuration changes.
- State the mitigation, verification, and follow-up actions separately.

## Answer Framework

1. Clarify functional and non-functional requirements.
2. State the simplest viable design.
3. Identify the consistency and failure assumptions.
4. Walk through a normal request and at least two failure cases.
5. Explain monitoring, recovery, and operational costs.
6. Compare alternatives and state why you chose one.

## Common Pitfalls

- Treating retries as a substitute for idempotency.
- Claiming a message broker removes the need for transactional design.
- Ignoring backpressure and retry storms.
- Using distributed locks without leases, fencing, and failure analysis.
- Quoting availability or throughput numbers without a workload model.
