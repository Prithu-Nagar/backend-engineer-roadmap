# Event-Driven Architecture

Day 27 introduces event-driven architecture as a way to decouple producers and
consumers through events.

## What Is Event-Driven Architecture?

In an event-driven system, a component publishes an event describing something
that happened. Other components consume that event and perform their own work.

```text
Order Service
     |
     | OrderCreated
     v
 Event Broker
     |
     +--------> Notification Service
     |
     +--------> Inventory Service
     |
     +--------> Analytics Service
```

The producer does not need to call every consumer directly.

## Event vs Command

An **event** describes something that has already happened.

```text
OrderCreated
PaymentCompleted
UserRegistered
```

A **command** asks a specific component to perform an action.

```text
CreateOrder
ChargePayment
SendNotification
```

The distinction helps define ownership and coupling between services.

## Why Use Events?

Event-driven architecture can provide:

- Loose coupling between services
- Asynchronous processing
- Independent consumer scaling
- Fan-out to multiple consumers
- Better isolation of slow downstream work
- A foundation for audit and integration workflows

## Typical Flow

```text
Producer
   |
   v
Event
   |
   v
Broker / Topic
   |
   +------> Consumer A
   |
   +------> Consumer B
   |
   +------> Consumer C
```

## Delivery and Reliability

Events introduce distributed-systems concerns that must be designed explicitly:

- At-least-once delivery can produce duplicates.
- Consumers should be idempotent when processing has side effects.
- Failed messages may need retries and dead-letter handling.
- Event schemas need compatibility rules.
- Ordering must be defined at the scope where it matters.
- Observability should connect producer and consumer activity.

## Trade-Offs

| Benefit | Cost |
|---|---|
| Loose coupling | More distributed behavior |
| Asynchronous processing | Eventual consistency |
| Fan-out | More consumers to operate |
| Independent scaling | Harder debugging |
| Failure isolation | More complex delivery semantics |

## Event Schema Example

```json
{
  "event_id": "evt-123",
  "event_type": "OrderCreated",
  "occurred_at": "2026-08-27T09:00:00Z",
  "version": 1,
  "data": {
    "order_id": 42,
    "user_id": 7
  }
}
```

A stable event envelope should make it possible to trace, validate, version,
and safely process events.

## When to Use It

Event-driven architecture is useful when multiple components react to the same
business event, when work can be asynchronous, or when direct service coupling
would make the system harder to evolve.

It is not automatically better than a synchronous request. For a simple
operation that needs an immediate result, direct request/response communication
may be easier to understand and operate.

---

## Day 28 — Event-Driven Architecture Trade-Offs

Day 28 revisits event-driven architecture from an architecture-decision
perspective. The goal is to decide when asynchronous events are worth the
additional operational complexity.

### Synchronous vs Event-Driven

Use synchronous communication when the caller needs an immediate result or
when the workflow is small and tightly coupled.

Use events when work can happen asynchronously, multiple consumers need the
same business fact, or downstream processing should be decoupled from the
request path.

```text
Synchronous
Client -> API -> Service -> Database -> Response

Event-driven
Client -> API -> Service -> Event Broker
                              |
                              +--> Consumer A
                              +--> Consumer B
                              +--> Consumer C
```

### Key Trade-Offs

| Decision | Event-Driven Benefit | Cost / Risk |
|---|---|---|
| Latency | Removes slow work from request path | Result may not be immediate |
| Coupling | Producers do not call every consumer | Event contracts become dependencies |
| Scaling | Consumers scale independently | More services to operate |
| Reliability | Failures can be isolated and retried | Duplicate delivery must be handled |
| Consistency | Supports asynchronous workflows | Eventual consistency becomes visible |
| Evolution | New consumers can subscribe later | Schema compatibility must be managed |
| Debugging | Durable events can aid reconstruction | Distributed tracing is harder |

### Queue vs Event Stream

A work queue is usually centered on distributing work so that a message is
processed by one consumer or consumer group. An event stream is commonly used
when multiple independent consumers need to observe the same event history.

The choice should follow the delivery and replay requirements rather than the
technology name alone.

### Decision Checklist

Before introducing event-driven communication, ask:

1. Does the caller really need a synchronous result?
2. Can the operation tolerate eventual consistency?
3. Will more than one consumer need the business event?
4. What happens if the event is delivered more than once?
5. How will failed events be retried or moved to a dead-letter destination?
6. How will event schemas evolve without breaking consumers?
7. What observability is required to trace a request across consumers?

Event-driven architecture is a useful tool, not a default architecture. The
simplest communication model that satisfies the reliability, latency, and
coupling requirements is usually the best starting point.
