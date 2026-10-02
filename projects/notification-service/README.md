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
