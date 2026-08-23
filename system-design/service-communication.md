# Service Communication — REST vs Async Messaging

Day 23 introduces the trade-off between synchronous REST communication and
asynchronous messaging when backend services need to exchange data or trigger
work in another service.

---

## Synchronous REST

A REST call creates a direct request/response dependency between services.

```text
Service A
   |
   | HTTP request
   v
Service B
   |
   | HTTP response
   v
Service A
```

The caller normally waits for the response before continuing.

### Strengths

- Simple request/response model
- Easy to understand and debug
- Immediate success/failure feedback
- Well suited to queries and operations that need a direct result

### Trade-offs

- Caller availability depends on the downstream service
- Network latency contributes directly to request latency
- Retries can amplify load if not designed carefully
- Long chains of synchronous calls can create tight coupling

---

## Asynchronous Messaging

With messaging, the producer publishes an event or command and a consumer
processes it later.

```text
Service A
   |
   | publish
   v
Message Broker
   |
   | deliver
   v
Service B
```

The producer does not have to wait for the consumer to finish the work.

### Strengths

- Decouples producer and consumer timing
- Supports background processing
- Helps absorb traffic spikes through queues
- Enables event-driven workflows
- A consumer can retry failed work independently

### Trade-offs

- More infrastructure and operational complexity
- Eventual consistency becomes common
- Debugging requires tracing messages across components
- Duplicate delivery must be handled safely
- Message ordering and delivery guarantees need explicit design

---

## Choosing the Model

Use synchronous REST when the caller needs an immediate answer:

```text
Client -> API -> Service -> Response
```

Use asynchronous messaging when the work can happen after the request:

```text
Client -> API -> Publish Event -> Response
                       |
                       v
                 Background Worker
```

Examples of good asynchronous candidates include email delivery, analytics,
search indexing, notification fan-out, and other work that does not need to
finish before the initial response.

---

## Failure Considerations

A production design should answer:

- What happens when the downstream service is unavailable?
- How many times can a message be retried?
- What happens to a message that repeatedly fails?
- Can the consumer safely process the same message twice?
- How is message ordering handled when it matters?
- How can an operation be traced across services?

For REST, timeouts, retries, and idempotency are important. For messaging,
delivery semantics, retry policies, dead-letter handling, and idempotent
consumers are important.

---

## Practical Rule

Prefer the simplest communication model that satisfies the workflow.

Do not introduce a message broker merely to make an architecture appear
more distributed. Use asynchronous messaging when decoupled processing,
traffic buffering, or event-driven behavior provides a concrete benefit.
