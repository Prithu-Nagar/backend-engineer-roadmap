# AI Reliability and Fallback Strategies

Day 58 focuses on reliability patterns for AI-backed services where external
models, retrieval systems, tools, and networks can fail independently.

---

## Failure Model

```text
Client
  |
  v
AI Service
  |
  +--> Retrieval
  |
  +--> LLM Provider
  |
  +--> Tool / External API
  |
  +--> Evaluation / Logging
```

Each dependency can fail, time out, return invalid data, or become temporarily
unavailable.

---

## Reliability Controls

Useful controls include:

- Explicit timeouts
- Bounded retries
- Exponential backoff with jitter
- Circuit breakers
- Concurrency limits
- Request cancellation
- Idempotency for retried mutations
- Structured error classification
- Dependency health signals

Retries should be limited to failures that are safe and useful to retry.

---

## Fallback Strategies

A fallback should be intentional rather than silently hiding a failure.

Examples:

| Failure | Possible fallback |
| --- | --- |
| Primary model unavailable | Secondary approved model |
| Retrieval unavailable | Cached or last-known-good context |
| Optional tool unavailable | Continue without optional tool |
| Streaming interrupted | Return partial result with explicit status |
| Non-critical enrichment fails | Serve core response without enrichment |

Fallback behavior should preserve security and authorization boundaries.

---

## Model Fallback

```text
Request
   |
Primary Model
   |
   +---- success ----> Response
   |
   +---- retryable failure
             |
             v
       Secondary Model
             |
             +---- success ----> Response
             |
             +---- failure ----> Controlled Error
```

A secondary model should not automatically receive data that the primary model
was not authorized to process.

---

## Timeouts and Retries

Set separate budgets for:

- Connection
- Provider response
- Tool execution
- Retrieval
- Overall request

Avoid unbounded retry loops. A retry should fit within the request's remaining
latency budget.

---

## Circuit Breaker

A circuit breaker can stop repeatedly sending requests to a dependency that is
known to be failing.

Typical states:

```text
CLOSED --> OPEN --> HALF-OPEN --> CLOSED
                    |
                    +-----------> OPEN
```

The half-open state allows a limited health-check workload before normal
traffic resumes.

---

## Graceful Degradation

Not every feature has equal importance.

For example:

```text
Core answer
    |
    +-- required retrieval ---- required
    |
    +-- optional metadata ----- degradable
    |
    +-- analytics event ------- asynchronous
```

The service should define which dependencies are required before the request
can succeed and which can be degraded.

---

## Safe Failure Responses

Do not expose provider credentials, internal prompts, raw stack traces, or
sensitive dependency payloads to clients.

Return stable application-level error categories such as:

- `DEPENDENCY_TIMEOUT`
- `DEPENDENCY_UNAVAILABLE`
- `INVALID_PROVIDER_RESPONSE`
- `REQUEST_CANCELLED`
- `AI_SERVICE_UNAVAILABLE`

Log detailed diagnostics internally with appropriate redaction.

---

## Reliability Checklist

1. Are dependency timeouts explicit?
2. Are retries bounded and limited to safe operations?
3. Is there a fallback for critical transient failures?
4. Can degraded behavior be identified by clients and operators?
5. Are authorization and tenant boundaries preserved during fallback?
6. Are sensitive details excluded from client-facing errors?
7. Are failures observable with stable error categories?
8. Can the service recover without manual intervention?
