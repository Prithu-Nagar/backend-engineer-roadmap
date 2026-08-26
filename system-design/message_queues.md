# Message Queues

Day 25 introduces message queues as a system-design tool for decoupling
backend components and handling asynchronous work.

## What Is a Message Queue?

A message queue is a buffer between producers that publish work and consumers
that process that work.

```text
Producer
   |
   v
Message Queue
   |
   +------> Consumer A
   |
   +------> Consumer B
```

The producer does not have to wait for the consumer to finish processing the
work.

## Why Use a Message Queue?

Queues are useful when a task:

- Does not need to complete before the HTTP response is returned.
- Is computationally expensive.
- Can be retried safely.
- Needs buffering during traffic spikes.
- Should be processed independently from the request service.
- Needs asynchronous fan-out to multiple consumers.

Examples include email delivery, report generation, image processing,
notifications, analytics events, and background jobs.

## Synchronous vs Asynchronous

### Synchronous

```text
Client -> API -> Service -> Dependency -> Response
```

The caller waits for the downstream operation.

### Asynchronous

```text
Client -> API -> Queue -> 202 Accepted
                       |
                       v
                    Worker
```

The API can acknowledge the request while a worker processes the task later.

## Important Queue Semantics

### At-Least-Once Delivery

A message may be delivered more than once. Consumers should therefore make
processing idempotent where possible.

### Retry

Failed messages can be retried with a bounded retry policy and backoff.

### Dead-Letter Queue

Messages that repeatedly fail can be moved to a dead-letter queue for
inspection and controlled recovery.

### Ordering

If ordering matters, the queue architecture must preserve ordering within the
required scope, such as a partition or key.

## Trade-Offs

| Benefit | Cost |
|---|---|
| Decouples services | Adds operational complexity |
| Absorbs traffic spikes | Processing becomes asynchronous |
| Enables retries | Duplicate delivery must be handled |
| Improves request latency | Monitoring becomes more involved |
| Supports background work | Eventual consistency may appear |

## When Not to Use a Queue

A queue is unnecessary when the operation is small, must return its result
immediately, and does not benefit from asynchronous processing. Introducing a
queue adds infrastructure and failure modes, so it should solve a real
architectural requirement.

## Backend Design Checklist

Before introducing a queue, define:

1. What event or job is being published?
2. Who owns the message schema?
3. How are retries handled?
4. Is processing idempotent?
5. What happens to permanently failing messages?
6. Does ordering matter?
7. How are queue depth and processing latency monitored?

---

## Day 26 — Queue Semantics

Day 26 focuses on the delivery guarantees that determine how consumers should
be implemented.

### At-Least-Once Delivery

At-least-once delivery prioritizes not losing a message, which means a consumer
may receive the same message more than once. The consumer should therefore use
an idempotency key or another deduplication strategy when processing has side
effects.

```text
Message
   |
   v
Consumer
   |
   +---- success ----> acknowledge
   |
   +---- failure ----> retry
                         |
                         v
                    dead-letter queue
```

### Consumer Design

A robust consumer should define:

1. How a message is identified uniquely.
2. Which operations are safe to repeat.
3. When acknowledgement occurs.
4. How retries are bounded.
5. When a failed message moves to a dead-letter queue.

The practical lesson is that queue reliability is not only a property of the
broker. Consumer-side idempotency and failure handling are part of the overall
design.
