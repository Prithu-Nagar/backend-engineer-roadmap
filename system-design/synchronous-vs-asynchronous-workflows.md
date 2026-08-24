# Synchronous vs Asynchronous Workflows

Day 24 focuses on deciding whether backend work should complete inside the
request/response path or continue asynchronously after the initial request.

---

## Synchronous Workflow

A synchronous workflow keeps the caller waiting for the operation to finish.

```text
Client
  |
  | request
  v
API
  |
  v
Service
  |
  v
Database / downstream service
  |
  | result
  v
API
  |
  | response
  v
Client
```

### Strengths

- Immediate result
- Straightforward control flow
- Simple error propagation
- Appropriate when the caller needs the result before continuing

### Trade-offs

- Request latency includes downstream work
- Slow dependencies can consume request resources
- Failures in a downstream service can directly affect the request
- Long synchronous chains increase coupling

---

## Asynchronous Workflow

An asynchronous workflow acknowledges the request before background work is
complete.

```text
Client
  |
  | request
  v
API
  |
  | publish job/event
  v
Queue / Broker
  |
  v
Worker
  |
  v
Database / downstream service
```

### Strengths

- Keeps slow work out of the request path
- Absorbs bursts through queueing
- Allows independent retry of background work
- Useful for workflows that do not require an immediate result

### Trade-offs

- Eventual consistency is common
- More operational components are required
- Failures need retry and dead-letter strategies
- Users may need a status endpoint or notification mechanism

---

## Choosing the Model

Prefer synchronous execution when the caller needs the result immediately:

- Fetching URL metadata
- Validating a request
- Creating a resource when the response must contain the created object

Prefer asynchronous execution when the work can finish later:

- Sending email
- Analytics aggregation
- Search indexing
- Notification fan-out
- Large background processing jobs

The decision should be based on user-visible latency, consistency needs,
failure behavior, and operational complexity rather than on whether an
architecture appears more distributed.

---

## Failure and Reliability Questions

A production design should explicitly answer:

- What timeout applies to synchronous dependencies?
- Can the synchronous operation be retried safely?
- What happens if an asynchronous worker crashes?
- How many times can a background job be retried?
- Can a job be processed more than once safely?
- How is job status exposed to clients when completion is asynchronous?

---

## Practical Rule

Use the simplest workflow that satisfies the business requirement. Moving work
asynchronously is valuable when it reduces request latency, isolates failures,
or provides useful buffering. It is not automatically better than a direct
request/response flow.
