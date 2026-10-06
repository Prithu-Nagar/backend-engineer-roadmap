# Notification System — Design Document

## Day 67

This project artifact turns the Notification Service LLD into a high-level
notification-system design that can be discussed in backend interviews.

---

## 1. Scope

The system accepts notification requests and delivers them asynchronously over
one or more channels.

The design extends the existing Day 63 Observer/Adapter LLD. The LLD remains
useful for in-process contracts; this document adds persistence, queues,
workers, retries, idempotency, and operational boundaries.

---

## 2. API Contract

### Create Notification

```http
POST /api/v1/notifications
Content-Type: application/json
```

Example request:

```json
{
  "recipient_id": 42,
  "channels": ["email", "push"],
  "template_id": "task-completed-v1",
  "data": {
    "task_id": 9001
  }
}
```

The API validates the request, persists durable intent, and returns
`202 Accepted` after the transaction commits.

### Status

```http
GET /api/v1/notifications/{notification_id}
```

The status response exposes durable notification and channel-level delivery
state according to the consistency contract.

---

## 3. Components

```text
Client
  |
  v
Notification API
  |
  +--> Notification DB
  |
  +--> Outbox
          |
          v
      Event Publisher
          |
          v
       Message Broker
       /      |            v       v       v
   Email     SMS     Push
   Worker   Worker   Worker
      |       |       |
      v       v       v
   Provider Provider Provider
```

Responsibilities:

- API: validation, authorization, transaction boundary.
- Database: durable notification and delivery state.
- Outbox publisher: converts committed intent into broker events.
- Broker: durable asynchronous transport.
- Workers: retries, idempotency, provider calls, and delivery state.
- Providers: external channel delivery.

---

## 4. State Model

```text
Notification:
CREATED -> QUEUED -> PROCESSING -> COMPLETED
                         |
                         +-> FAILED

Delivery:
PENDING -> SENT
    |
    +-> RETRY_WAIT -> PENDING
    |
    +-> FAILED
```

A notification can be `COMPLETED` only when the product's defined success
criteria have been met. A partially successful multi-channel notification must
retain channel-level state.

---

## 5. Event Contract

```json
{
  "event_id": "evt-123",
  "event_type": "notification.requested",
  "schema_version": 1,
  "notification_id": 1001,
  "recipient_id": 42,
  "channel": "email",
  "template_id": "task-completed-v1",
  "payload": {
    "task_id": 9001
  }
}
```

`event_id` is unique and is used as part of duplicate detection and tracing.

---

## 6. Delivery Semantics

The system assumes at-least-once event processing.

Workers must therefore be safe when an event is delivered more than once.

Recommended idempotency key:

```text
notification:{notification_id}:channel:{channel}
```

The delivery record should be checked before invoking a provider when possible.
Provider calls should also reuse an idempotency key when the provider supports
one.

---

## 7. Retry Policy

Retry only failures that are plausibly transient:

- Network timeout
- Temporary provider unavailability
- Rate-limit response
- Explicit transient provider error

Do not retry permanent validation or recipient errors indefinitely.

Use bounded exponential backoff with jitter and move exhausted attempts to a
dead-letter workflow for investigation.

---

## 8. Capacity and Scaling

The API and channel workers scale independently.

Primary capacity indicators:

- Requests per second
- Pending outbox rows
- Broker messages per second
- Queue age
- Worker concurrency
- Provider quota
- Average and tail provider latency

Per-channel queues prevent a slow provider from consuming the capacity needed
by other channels.

---

## 9. Reliability

The critical reliability boundary is the database transaction:

```text
business state change
        +
notification intent
        |
        v
     COMMIT
        |
        v
outbox publication
```

Never publish a notification event before the transaction that establishes its
durable intent has committed.

---

## 10. Security and Data Boundaries

- Authorize the caller before creating notification requests.
- Do not place secrets in event payloads.
- Minimize personally identifiable recipient data in broker messages.
- Encrypt sensitive data at rest and in transit according to the deployment
  requirements.
- Apply tenant boundaries to notification lookup and delivery state.
- Keep provider credentials in managed secret storage rather than source code.

---

## 11. Project Implementation Path

Future implementation increments can proceed in this order:

1. Keep the existing Day 63 LLD contracts.
2. Add durable notification and delivery models.
3. Add transactional outbox persistence.
4. Add a broker adapter with an in-memory test implementation.
5. Add channel workers with deterministic retry behavior.
6. Add idempotency and dead-letter handling.
7. Add metrics, tracing, and integration tests.
8. Replace in-memory adapters with production infrastructure.

The design is intentionally framework-neutral so it can later be implemented
with Flask, FastAPI, Django, or another backend stack without changing the core
architecture.
