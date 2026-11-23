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
