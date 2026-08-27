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
