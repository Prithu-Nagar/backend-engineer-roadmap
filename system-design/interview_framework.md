# System Design Interview Framework

Use this repeatable structure for HLD interview questions. State assumptions
explicitly and keep the design proportional to the problem.

## 1. Clarify requirements

- Functional: actors, core use cases, read/write flows, and out-of-scope features.
- Non-functional: latency, availability, durability, consistency, privacy, and
  security targets.
- Confirm scale, geography, retention, freshness, and acceptable degradation.

## 2. Estimate capacity

Write assumptions before calculating. For example:

- Average RPS = daily requests / 86,400.
- Peak RPS = average RPS × peak multiplier.
- Raw storage = records per day × average record size × retention days.
- Include replication, indexes, metadata, and growth separately.

Use round numbers and identify which estimate could change the architecture.

## 3. Define APIs and data model

List the primary endpoints, request/response shape, pagination strategy, error
codes, authentication, authorization, and idempotency requirements. Identify
entities, ownership boundaries, indexes, uniqueness constraints, and retention.

## 4. Draw the high-level design

Start with client, edge/API layer, application services, durable database, and
external dependencies. Add cache, queue, search, or object storage only when a
requirement justifies it. Trace one read and one write request end to end.

## 5. Analyze bottlenecks and failures

Discuss hot keys, expensive queries, connection pools, cache misses, queue lag,
fan-out, dependency timeouts, retries, duplicate delivery, and partial failure.
Explain timeouts, bounded retries with jitter, backpressure, and graceful
degradation. Define what is measured and alerted on.

## 6. Explain trade-offs

Compare consistency and availability where relevant, synchronous and
asynchronous work, read/write amplification, operational complexity, and cost.
Avoid invoking CAP as a blanket statement: specify the network partition and
which operation must preserve which guarantee.

## Interview closing checklist

- Did I distinguish assumptions from facts?
- Did I cover authorization and abuse controls?
- Did I identify the source of truth and consistency needs?
- Did I explain scaling limits and a credible failure path?
- Did I name key metrics and the next bottleneck?
- Can I defend why each major component is present?
