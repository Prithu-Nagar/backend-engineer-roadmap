# Notification Service — LLD

## Day 63

This learning artifact applies Observer and Adapter patterns to a small
notification service.

### Design

```text
NotificationService
        |
        v
NotificationSubject
     /        \
    v          v
 Audit       EmailAdapter
 Observer        |
                 v
          EmailProvider
```

### Responsibilities

- `NotificationService` validates the application-level notification and starts
  the use case.
- `NotificationSubject` manages subscribers and publishes notifications.
- `AuditObserver` records notification events without changing the service.
- `EmailAdapter` translates the application's observer contract to an external
  provider interface.
- `EmailProvider` represents provider-specific infrastructure.

### LLD Principles

- Depend on small protocols rather than concrete integrations.
- Keep provider-specific interfaces at the infrastructure edge.
- Use composition to assemble the notification workflow.
- Keep validation in the application boundary.
- Make subscriber ownership explicit.
- Allow additional channels to be added without changing the notification
  service's core workflow.

### Production Considerations

A production implementation would normally add:

- Persistent notification and delivery state
- Idempotency keys
- Retry and backoff policies
- Dead-letter handling
- Per-provider timeouts and circuit breakers
- Asynchronous queue-based delivery
- Delivery metrics and structured logs
- Template/version management
- Tenant and recipient authorization boundaries

The implementation is intentionally deterministic and provider-light so the LLD
boundaries can be reviewed without requiring an external service.

---

## Day 67 — Notification System Design

Day 67 extends the existing Notification Service LLD into an HLD-oriented
notification system design.

Added:

- `notification_system_design.md`

The design covers:

- API contract and asynchronous request flow
- Transactional outbox and durable event intent
- Message-broker and channel-worker architecture
- At-least-once delivery and idempotency
- Retry, backpressure, and dead-letter handling
- Per-channel scaling and provider isolation
- Notification/delivery state models
- Security, observability, and capacity considerations

The Day 63 Observer/Adapter LLD remains unchanged. The Day 67 artifact adds
distributed-system boundaries around that earlier object-level design.

## Runnable notification API and local worker

The project now includes a runnable Flask API, notification domain model,
in-memory enqueue service, worker abstraction, and local provider adapter.

Start the API from the repository root:

```bash
python projects/notification-service/app.py
```

Create a notification:

```bash
curl -X POST http://127.0.0.1:5000/notifications \\
  -H "Content-Type: application/json" \\
  -d '{"recipient":"person@example.com","channel":"email","message":"Hello"}'
```

The API returns `202 Accepted` with the notification identifier and `queued`
status. Inspect it with `GET /notifications/<notification_id>`. Process one
queued item using `POST /notifications/process-next`; the local provider
records the delivery in process memory and the notification becomes `sent`.
Transient provider failures are retried with bounded exponential backoff; exhausted or permanent failures are captured as `failed` delivery status. Requests can include an `Idempotency-Key` header (or `idempotency_key` field) to prevent duplicate enqueueing. Reusing a key with a different payload returns `409 Conflict`. API responses also include a generated `X-Request-ID`, `X-Content-Type-Options: nosniff`, and `Cache-Control: no-store` headers.

Run focused tests:

```bash
python -m pytest projects/notification-service/tests -q
```

The current queue, notification store, and local provider are in-memory demo
adapters. They are not durable across restarts, do not contact a real email/SMS/
push provider. Retry and idempotency behavior is implemented for the in-memory
demo workflow, but queue state and idempotency records are lost on restart.


## Retry and duplicate protection

- `Idempotency-Key` may be supplied as an HTTP header or as `idempotency_key`
  in the JSON request. Repeating the same key and payload returns the original
  notification without adding another queue item; a different payload with the
  same key returns `409 Conflict`.
- Connection and timeout failures are treated as transient and retried up to
  three attempts by default, with exponential delays (1s, then 2s). Permanent
  provider errors are not retried. Exhausted requests retain `failed` status
  and the last error; successful requests retain provider delivery identifiers.
- The in-memory adapter demonstrates bounded retry and request deduplication,
  not durable idempotency across restarts or exactly-once external delivery.


## Day 24 — Delivery guarantees, queue decision, and acceptance demo

### Queue choice for this MVP

The runnable implementation deliberately uses Python's thread-safe
`queue.Queue` as a **process-local FIFO queue**. It is dependency-free, makes
enqueue/worker behavior deterministic in tests, and is sufficient for a single
process demo. The queue is not persistent, shared across processes, bounded by
a configured capacity, or suitable for horizontal worker scaling. Both queued
items and the in-memory notification/idempotency stores are lost on restart.

For a multi-process deployment, replace this adapter boundary with a durable
broker (for example, RabbitMQ or Redis Streams) and persist notification and
idempotency state in a database. Select the broker based on operational
requirements: acknowledgement/redelivery behavior, ordering needs, retention,
consumer-group support, dead-letter routing, throughput, and operational
complexity. Do not treat swapping only the queue while leaving state in memory
as a durable production implementation.

### Delivery guarantee and failure window

- The demo provides FIFO enqueueing and bounded retries for connection/time-out
  failures. Retry delays are exponential and deterministic in tests.
- Idempotency keys suppress duplicate enqueue requests while the process is
  alive; reusing a key with a different payload is rejected.
- Processing is **at-least-once in intent, not exactly-once delivery**. A worker
  can call a provider successfully and then crash before recording `sent`;
  a redelivered item could therefore send twice. Use a stable delivery key and
  provider-side idempotency where supported.
- Permanent provider errors are not retried. Exhausted transient failures end
  in `failed` with the last error retained.
- The local provider records messages in memory and does not send real email,
  SMS, or push notifications. The current API has no authentication, durable
  outbox, dead-letter broker, or cross-process coordination; those are explicit
  MVP limitations.

### Run the deterministic end-to-end demo

From the repository root:

```bash
python projects/notification-service/demo.py
```

The demo enqueues one request, repeats it with the same idempotency key,
simulates one transient provider outage, retries, and prints the final delivery
status. It uses an in-process local provider and performs no external delivery.

### Acceptance gate

Run from the repository root:

```bash
python -m pytest projects/notification-service/tests -q
python projects/notification-service/demo.py
```

The test suite covers API validation/status responses, duplicate request
handling, key conflicts, successful local delivery, transient retry/backoff,
retry exhaustion, permanent failure, and empty-queue behavior. Record actual
command output when presenting verification; this README does not imply that a
remote broker, external provider, or production deployment has been tested.
