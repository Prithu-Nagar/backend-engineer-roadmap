# LLD — Observer and Adapter Patterns

## Goal

Use Observer to decouple event producers from multiple subscribers, and Adapter
to integrate an external component whose interface does not match the service
contract.

## Observer Pattern

Observer creates a one-to-many relationship between a subject and subscribers.

```text
Notification Service
        |
        v
 NotificationSubject
     /        \
    v          v
 AuditObserver  SmsAdapter
                  |
                  v
            External SMS Client
```

The subject owns subscription management and publishes events through a stable
observer contract. Subscribers can be added or removed without changing the
publisher's core workflow.

### Backend Use Cases

- Notification fan-out
- Domain events
- Audit logging
- Cache invalidation
- Metrics/event consumers
- In-process lifecycle hooks

### Design Considerations

- Keep the event payload small and stable.
- Prevent duplicate subscriptions where identity matters.
- Decide whether observer failures should stop publication or be isolated.
- Use asynchronous delivery when subscribers can be slow or remote.
- Define ownership and lifecycle of subscriptions explicitly.

## Adapter Pattern

Adapter translates one interface into another expected by the application.

```text
Application Contract
        |
        v
NotificationObserver
        |
        v
     SmsAdapter
        |
        v
ExternalSmsClient
```

The application depends on the stable contract rather than the third-party
client's method names or request format.

### Backend Use Cases

- Email/SMS/push providers
- Payment gateways
- Storage clients
- Legacy SDKs
- Metrics and tracing libraries
- Cloud-provider-specific clients

## Observer + Adapter Together

A notification service can publish one event to several observers while each
integration remains isolated behind its adapter.

```text
                 +--> Audit Observer
                 |
Notification --->+--> Email Adapter ---> Email Provider
                 |
                 +--> SMS Adapter ----> SMS Provider
```

This separates event fan-out from provider-specific integration details.

## Failure and Reliability Boundaries

For production systems, avoid assuming that all observers complete instantly.

Consider:

- Per-observer timeouts
- Retry policy for transient provider failures
- Dead-letter handling for repeated delivery failures
- Idempotency keys for notification delivery
- Circuit breakers around unstable providers
- Structured delivery status and attempt tracking
- Metrics for success, failure, latency, and retries

An asynchronous queue is usually preferable when notification delivery must not
block the primary request path.

## Trade-offs

Observer is useful for loose coupling, but excessive in-process subscribers can
make control flow harder to trace. Adapter adds a small abstraction layer, but
it keeps third-party contracts at the infrastructure boundary.

Use the patterns when the separation improves changeability, testing, or
integration boundaries; do not add them merely because a pattern exists.

## Review Checklist

- Is the observer contract small and stable?
- Can subscribers be added without modifying the subject's core logic?
- Are subscriber failures isolated appropriately?
- Does the adapter translate only interface differences?
- Are external provider details kept outside application policy?
- Are retries, idempotency, and delivery status explicit where required?
- Would asynchronous delivery be safer for slow or remote observers?
