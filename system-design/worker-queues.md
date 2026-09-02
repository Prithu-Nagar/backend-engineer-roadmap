# Worker Queues

Day 33 introduces worker queues as an architecture for moving asynchronous
work out of the request path.

## Core Model

A producer creates a job and places it on a queue. A worker consumes the job
and performs the work independently of the original request.

```text
Client
  |
  v
API Service
  |
  | enqueue job
  v
Worker Queue
  |
  +----> Worker A
  |
  +----> Worker B
```

The API can acknowledge work without waiting for the background operation to
finish when the product requirements allow asynchronous processing.

## Why Use Worker Queues?

Worker queues are useful for work that:

- Does not need to complete before the HTTP response.
- Can tolerate asynchronous completion.
- May be expensive or slow.
- Benefits from retry handling.
- Needs buffering during traffic spikes.
- Can be scaled independently from API traffic.

Examples include report generation, notifications, analytics aggregation,
image processing, and scheduled maintenance.

## Producer / Consumer Responsibilities

### Producer

The producer should:

1. Validate the job input.
2. Create a stable job identifier where needed.
3. Publish a well-defined message.
4. Decide whether the request should wait for completion.

### Worker

The worker should:

1. Validate the received message.
2. Execute the job with a bounded timeout.
3. Acknowledge only after successful processing when the queue semantics require
   it.
4. Retry transient failures.
5. Send permanently failing jobs to a dead-letter mechanism when supported.

## Delivery and Failure Semantics

A queue does not remove the need for failure handling.

### At-Least-Once Delivery

A job may be delivered more than once. Side-effecting workers should therefore
use idempotency keys or another deduplication strategy.

### Retry

Retries should distinguish transient failures from permanent failures. A
bounded retry policy with backoff prevents a failing dependency from consuming
all worker capacity.

### Dead-Letter Queue

Jobs that repeatedly fail can be moved aside for inspection and controlled
reprocessing instead of retrying forever.

### Ordering

If jobs must be processed in order, define the required ordering scope. Global
ordering can reduce parallelism, while partition- or key-based ordering often
allows more throughput.

## Scaling Workers

Worker capacity can be scaled independently from the API tier.

```text
                 +---- Worker 1
Queue ----------+---- Worker 2
                 +---- Worker 3
```

Useful signals include:

- Queue depth
- Oldest job age
- Processing latency
- Success/failure rate
- Retry count
- Worker utilization
- Dead-letter volume

A growing queue with increasing job age is a capacity signal, not merely an API
latency metric.

## Background Jobs vs In-Process Tasks

An in-process background task is simple but shares resources and lifecycle with
the application instance. A durable external queue and separate workers provide
stronger isolation and independent scaling.

```text
Simple / local:
API process -> in-process task

Distributed:
API -> durable queue -> worker fleet
```

For production systems, choose the simplest mechanism that meets durability,
retry, scaling, and failure-recovery requirements.

## Backend Design Checklist

Before introducing a worker queue, define:

1. What work is asynchronous?
2. What is the job payload and versioning strategy?
3. Is processing idempotent?
4. What is the acknowledgement point?
5. Which failures are retryable?
6. What is the retry limit and backoff policy?
7. What happens to permanently failing jobs?
8. How is queue backlog monitored?
9. Can workers scale independently?
10. What happens when the worker fleet is unavailable?
