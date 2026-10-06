# Notification System — HLD

## Day 67

Day 67 applies the HLD process to a notification system that accepts
notification requests, persists durable delivery intent, and asynchronously
delivers through multiple channels.

---

## 1. Requirements

### Functional Requirements

- Accept notification requests for a user or recipient.
- Support multiple channels such as email, SMS, and push.
- Persist notification and delivery state.
- Process delivery asynchronously.
- Retry transient provider failures.
- Prevent duplicate delivery where the provider and contract support idempotency.
- Expose delivery status and failure information.
- Allow templates and channel preferences to evolve independently.

### Non-Functional Requirements

- Low latency for accepting a notification request.
- Durable event capture before acknowledging a request.
- Horizontally scalable workers.
- At-least-once event processing with idempotent consumers.
- Backpressure when providers or downstream systems are slow.
- Observable queue depth, delivery latency, retries, and permanent failures.

Non-goals for the first version:

- Guaranteed exactly-once delivery across arbitrary external providers.
- A single synchronous request that waits for every channel to finish.
- Global ordering across all users and channels.

---

## 2. High-Level Architecture

```text
Client
  |
  v
API Gateway
  |
  v
Notification API
  |
  +----> Notification DB
  |           |
  |           v
  |      Outbox Events
  |           |
  |           v
  |      Event Publisher
  |           |
  |           v
  |      Message Broker
  |        /    |      |       v     v     v
  |    Email   SMS   Push Workers
  |       |     |      |
  |       v     v      v
  |    Providers / External Services
  |
  +----> Status API
```

The API owns request validation and durable intent. Workers own asynchronous
delivery and provider-specific retry behavior.

---

## 3. Request Flow

```text
POST /notifications
        |
        v
validate request
        |
        v
begin transaction
        |
        +--> persist notification
        |
        +--> persist outbox event
        |
        v
commit
        |
        v
return 202 Accepted
        |
        v
outbox publisher -> broker -> channel worker
```

The outbox prevents the classic failure where a database transaction commits
but the application crashes before publishing the corresponding event.

---

## 4. Event Contract

A notification event can contain:

| Field | Purpose |
|---|---|
| `event_id` | Globally unique event identifier |
| `event_type` | Stable semantic event name |
| `notification_id` | Durable notification reference |
| `recipient_id` | Application-level recipient |
| `channel` | Email, SMS, push, etc. |
| `template_id` | Versioned rendering contract |
| `payload` | Channel-independent business data |
| `created_at` | Event creation time |
| `schema_version` | Contract evolution |

Consumers should tolerate additive fields and explicitly handle unsupported
schema versions.

---

## 5. Queue and Worker Design

Separate queues can be useful when channels have different throughput and
failure characteristics.

```text
                 +--> email.queue --> email workers
notification --->+--> sms.queue   --> sms workers
                 +--> push.queue  --> push workers
```

Workers should:

1. Claim an event.
2. Check idempotency state.
3. Render the required template.
4. Call the provider with a bounded timeout.
5. Record success or a retryable failure.
6. Retry with exponential backoff and jitter when appropriate.
7. Move permanently failing events to a dead-letter path.

Backpressure should be visible through queue depth and processing latency rather
than hidden by unlimited in-memory concurrency.

---

## 6. Reliability and Delivery Semantics

The recommended baseline is **at-least-once processing**.

Why:

- Brokers can redeliver messages.
- Workers can crash after provider acceptance but before persisting success.
- Network failures can make provider outcomes ambiguous.

Therefore, delivery should use an idempotency key such as:

```text
notification:{notification_id}:channel:{channel}
```

If the provider supports idempotency keys, pass the same key on retries.

Exactly-once end-to-end delivery is not assumed because the external provider is
outside the database transaction boundary.

---

## 7. Ordering

Global ordering is usually unnecessary and expensive.

If a product requires per-user ordering:

- Partition events by a stable user key.
- Preserve order within the selected partition.
- Avoid making one slow recipient block unrelated users.

Ordering requirements should be stated at the business level before adding
partitioning complexity.

---

## 8. Failure Modes

| Failure | Response |
|---|---|
| Notification API unavailable | Load balance and retry at client boundary |
| Database unavailable | Reject/timeout rather than acknowledge durable intent |
| Outbox publisher unavailable | Keep committed outbox rows for later publication |
| Broker unavailable | Buffer only within bounded infrastructure; alert |
| Provider timeout | Retry with bounded exponential backoff |
| Permanent provider rejection | Mark failed and use dead-letter handling |
| Duplicate event | Idempotency check prevents duplicate work |
| Worker crash | Broker redelivery / lease expiry enables recovery |

---

## 9. Scaling

Scale independently:

- API instances by request rate.
- Outbox publishers by pending-row volume.
- Broker partitions by event throughput.
- Channel workers by provider latency and quota.
- Status reads with replicas or caches when the consistency contract permits.

Avoid scaling a single worker pool indefinitely. Per-channel queues make
capacity and provider limits explicit.

---

## 10. Data Model

Core durable entities:

```text
Notification
  |
  +----< NotificationDelivery
  |
  +----< OutboxEvent
```

`NotificationDelivery` tracks channel-specific state such as attempts,
provider response, next retry time, and final status.

The outbox is an integration boundary, not a replacement for the notification
domain model.

---

## 11. Observability

Track at least:

- Accepted notification rate
- Outbox pending count and age
- Broker queue depth
- Worker throughput
- Delivery success/failure rate by channel
- Retry count
- Dead-letter count
- Provider latency and timeout rate
- End-to-end notification latency
- Duplicate/idempotency suppression count

Correlate API request IDs, event IDs, notification IDs, and provider request IDs.

---

## 12. Key Trade-offs

### Synchronous vs Asynchronous Delivery

Asynchronous delivery improves API latency and isolates provider failures, at the
cost of eventual delivery and more operational components.

### Single Queue vs Per-Channel Queues

A single queue is simpler. Per-channel queues provide isolation when providers
have different quotas, latency, or reliability characteristics.

### Polling Outbox vs CDC

Polling is straightforward and database-local. Change Data Capture can reduce
polling overhead but adds infrastructure and operational coupling.

### At-Least-Once vs Exactly-Once

At-least-once processing with idempotent consumers is the practical baseline.
Exactly-once claims should not be made merely because a broker or database
supports a transactional feature.

---

## 13. Interview Explanation

Explain the design in this order:

1. Define notification channels and delivery requirements.
2. Separate request acceptance from asynchronous delivery.
3. Persist notification state and outbox intent in one transaction.
4. Publish events to a durable broker.
5. Isolate workers and provider-specific behavior.
6. Use at-least-once processing with idempotency.
7. Add retries, backpressure, and dead-letter handling.
8. Scale API, broker, and workers independently.
9. Explain ordering and failure trade-offs.
10. Finish with observability and capacity assumptions.

The central principle is: **acknowledge durable intent first, then perform
delivery asynchronously with explicit delivery semantics.**
