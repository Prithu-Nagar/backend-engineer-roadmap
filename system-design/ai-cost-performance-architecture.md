# AI Cost / Performance Architecture

## Goal

Design an AI-backed service that controls model spend while meeting endpoint
latency and reliability requirements.

The architecture should make cost, latency, throughput, and quality visible at
the same request boundary rather than optimizing one metric in isolation.

## Request Flow

```text
Client
  |
  v
API Gateway / Edge
  |
  +--> Authentication + Tenant Context
  |
  +--> Rate Limiter / Quota
  |
  v
AI Request Service
  |
  +--> Cache
  |
  +--> Request Classification
  |       |
  |       +--> Fast / low-cost model
  |       +--> Standard model
  |       +--> High-capability model
  |
  +--> Context Reduction / Retrieval
  |
  v
Model Provider
  |
  v
Response Validation
  |
  +--> Usage + Latency + Cost Metrics
  |
  v
Client
```

## Main Cost Drivers

- Input tokens
- Output tokens
- Model-specific pricing
- Repeated or duplicated prompts
- Unbounded conversation history
- Retrieval that adds unnecessary context
- Retries and fallback calls
- Low cache effectiveness
- Excessive tool/model round trips

## Latency Budget

A useful request budget separates the major components:

```text
Total latency
= queueing
+ authentication
+ retrieval
+ prompt construction
+ model latency
+ tool calls
+ response validation
+ transport
```

Track at least:

- p50 latency
- p95 latency
- p99 latency
- time spent waiting for the provider
- time spent retrieving context
- time spent in tool calls

Average latency alone can hide tail-latency problems.

## Model Selection

Use a policy layer rather than selecting a model ad hoc in every route.

Example policy inputs:

- Task type
- Required quality level
- Input size
- Expected output size
- Latency target
- Tenant quota
- Current provider health
- Cache availability

A simple policy can route short, latency-sensitive requests to a faster model,
while larger or quality-sensitive requests use a more capable model.

Model selection should remain configurable because provider prices, latency,
and capabilities change over time.

## Token Management

Reduce unnecessary context before optimizing infrastructure.

Useful controls:

- Trim irrelevant conversation history
- Summarize older messages
- Retrieve only relevant documents
- Cap retrieved chunks
- Limit maximum output tokens
- Avoid repeating system instructions unnecessarily
- Cache stable prompt components where supported
- Detect duplicate requests

Token budgets should be explicit per endpoint and, where appropriate, per
tenant.

## Caching

Useful cache candidates include:

- Deterministic or near-deterministic requests
- Reusable retrieval results
- Stable system configuration
- Expensive intermediate computations

Cache keys should include the inputs that materially affect correctness, such
as model version, prompt version, tenant scope, and relevant request parameters.

Never allow a cache to bypass tenant isolation or authorization.

## Rate Limiting and Quotas

AI endpoints should usually have more than one control:

- Requests per second
- Concurrent in-flight requests
- Tokens per minute
- Daily or monthly cost budget
- Per-tenant quotas
- Per-endpoint limits

Rate limiting protects latency and provider capacity; quotas protect spend.
They solve related but different problems.

## Reliability vs Cost

Retries can increase cost because a failed model call may be billed before the
application retries it.

Use:

- Bounded retry counts
- Exponential backoff with jitter
- Retry only transient failures
- Explicit timeout budgets
- Circuit breakers for unhealthy providers
- Fallback models only when the quality policy permits

Record every provider attempt so usage analytics do not undercount retry cost.

## Observability

Record a request-level usage event containing:

- Tenant
- Endpoint
- Provider
- Model
- Prompt/pipeline version
- Input tokens
- Output tokens
- Latency
- Estimated cost
- Cache hit
- Retry count
- Outcome/error category

Useful dashboards include:

- Cost by tenant
- Cost by model
- Cost per successful request
- Token usage by endpoint
- p95/p99 latency
- Provider error rate
- Cache-hit rate
- Rate-limit rejection rate

## Capacity Planning

Separate three resource dimensions:

1. **Request throughput** — requests per second.
2. **Token throughput** — input/output tokens per minute.
3. **Spend** — estimated currency cost per time period.

A service can be within request-rate limits while still exceeding token or cost
budgets.

## Trade-offs

| Optimization | Typical benefit | Main risk |
| --- | --- | --- |
| Smaller/faster model | Lower cost and latency | Lower task quality |
| Smaller context | Lower cost and latency | Missing relevant information |
| Aggressive caching | Lower cost and latency | Stale or incorrect reuse |
| More retries | Higher success rate for transient failures | Higher latency and cost |
| Strict rate limits | Stable capacity and spend | More rejected requests |
| Batch processing | Better throughput efficiency | Higher completion latency |
| High-capability model | Better performance on difficult tasks | Higher cost/latency |

## Design Principle

Treat AI cost and performance as first-class service concerns. The application
should be able to explain where tokens, latency, retries, and spend are going,
then apply explicit policies for model selection, context size, caching, rate
limits, and graceful degradation.
