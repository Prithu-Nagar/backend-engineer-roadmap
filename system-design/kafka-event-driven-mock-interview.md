# Kafka and Event-Driven Architecture — Mock Interview

Use this scenario to practice event-driven design, delivery guarantees, partitioning, idempotency, and operational failure handling.

## Scenario

A task-management service must publish task-created and task-updated events so notification, analytics, and search-indexing consumers can process changes independently. Some consumers may be temporarily unavailable, and duplicate delivery must not create duplicate side effects.

## 1. Clarify Requirements

Ask about event volume, peak throughput, acceptable processing delay, ordering requirements, retention, replay needs, data sensitivity, and recovery objectives. Identify which operations must be synchronous and which can complete asynchronously.

## 2. Propose the Flow

1. The API validates and commits the task update in the database.
2. A transactional outbox row is written in the same database transaction.
3. An outbox publisher sends the event to Kafka and records publication progress.
4. Consumers process events and commit offsets only after their durable work succeeds.
5. Consumer failures are retried with bounded policies; poison events are isolated for inspection and replay.

The outbox avoids the unsafe dual-write pattern in which the database commits but event publication is lost, or vice versa.

## 3. Topics, Keys, and Schemas

- Choose a topic boundary based on event purpose, access, retention, and throughput.
- Key task events by `task_id` when per-task ordering is required.
- Partition count affects parallelism and key distribution; hot keys can still bottleneck a partition.
- Include event ID, event type, schema version, entity ID, occurrence time, and trace/correlation ID.
- Evolve schemas compatibly and avoid placing secrets or unnecessary personal data in events.

Kafka ordering is guaranteed within a partition, not globally across a topic.

## 4. Delivery and Idempotency

Kafka can provide at-least-once processing patterns, so consumers should assume duplicates are possible. Use an event ID or business idempotency key and persist deduplication state atomically with the consumer's side effect when possible.

Kafka producer idempotence and transactions help with Kafka-level guarantees, but they do not automatically make an external database or API side effect exactly once.

## 5. Failure Modes and Operations

Discuss broker unavailability, consumer crashes, rebalances, lag growth, malformed events, schema incompatibility, poison messages, and downstream outages. Monitor consumer lag, publish failures, retry counts, dead-letter volume, processing latency, and partition skew.

Define retry limits, backoff, dead-letter access controls, replay procedures, and alert thresholds. Replaying events must be safe and observable.

## 6. Trade-offs and Follow-up Questions

- Why use Kafka instead of a task queue?
- When is a simpler queue sufficient?
- How do you preserve ordering for one entity?
- How do you handle a database write succeeding while event publication fails?
- What happens when a consumer is slower than producers for several hours?
- How would you reprocess events after fixing a consumer bug?

A strong answer states assumptions, names the guarantees precisely, and explains how correctness is tested and monitored.
