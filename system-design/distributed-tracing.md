# Distributed Tracing Basics

Day 37 introduces distributed tracing as the system-design counterpart to
structured logging and database observability.

## Why Tracing Matters

A single user request can cross several services:

```text
Client
  |
  v
API Gateway
  |
  v
Expense API
  |   |  +--> Redis
  |
  +-----> PostgreSQL
```

Logs from individual services answer local questions. A trace connects the
work performed by those services into one request path.

## Trace and Span

A **trace** represents one end-to-end operation.

A **span** represents one timed unit of work inside that trace.

```text
Trace: GET /expenses/42

+---------------- API request ----------------+
|                                             |
|  +-- database query --+                     |
|  |                    |                     |
|  +--------------------+                     |
|                                             |
|                  +-- Redis lookup --+       |
|                  |                  |       |
|                  +------------------+       |
+---------------------------------------------+
```

Typical span fields include:

- Trace ID
- Span ID
- Parent span ID
- Service name
- Operation name
- Start and end timestamps
- Status
- Selected attributes

## Correlation IDs vs Trace IDs

A correlation ID is a simple application-level identifier used to connect
related log records.

A trace ID belongs to a tracing model and can connect a tree of spans across
services.

They can coexist:

| Signal | Main purpose |
| --- | --- |
| Correlation ID | Group application log events |
| Trace ID | Follow an end-to-end request |
| Span ID | Identify one operation within a trace |
| Metrics | Quantify system behavior over time |

## Propagation

When Service A calls Service B, tracing context must cross the service
boundary.

```text
Service A
  trace=abc
  span=001
      |
      | trace context
      v
Service B
  trace=abc
  parent=001
  span=002
```

The downstream service creates a child span instead of starting an unrelated
trace for the same request.

## Sampling

Tracing every request can create significant storage and processing cost.

Common strategies include:

- Head-based sampling
- Tail-based sampling
- Higher sampling for errors
- Higher sampling for slow requests

Sampling should preserve enough diagnostic information to investigate important
failures and latency outliers.

## Instrumentation Boundaries

Useful span boundaries in a backend service include:

- HTTP request handling
- Outbound HTTP calls
- Database queries
- Redis operations
- Background jobs
- Message publication and consumption

Avoid creating a span for every tiny function. Excessive instrumentation can
increase noise and telemetry overhead.

## Failure and Latency Analysis

Tracing helps answer questions such as:

1. Which downstream service added most of the latency?
2. Did the request fail before or after the database call?
3. Are slow requests concentrated around one dependency?
4. Are retries multiplying downstream work?
5. Which endpoint generates the largest number of expensive spans?

## Logs, Metrics, and Traces

Observability is strongest when the three signals are connected.

```text
Metrics  -> What is happening?
Logs     -> What happened?
Traces   -> Where did it happen?
```

A practical backend can put the trace ID and correlation ID into structured log
records so an operator can move from a latency metric to a trace and then to
the relevant application or database logs.

## Interview Questions

1. What is the difference between a trace and a span?
2. How is tracing context propagated between services?
3. Why might a system sample traces?
4. When is a correlation ID useful even without a tracing platform?
5. How would you connect logs, metrics, traces, Redis, and database activity
   during a production incident?
