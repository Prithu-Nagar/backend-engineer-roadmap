# System Design Review — Day 70

## Purpose

Day 70 consolidates the System Design & LLD phase into a portfolio pack and a timed review. The goal is to explain architecture decisions, identify bottlenecks, compare trade-offs, and reason about CAP during partitions—not simply recall component names.

## HLD Review Checklist

### Requirements and capacity

- Separate functional requirements from latency, availability, durability, consistency, and security goals.
- Write down assumptions for read/write ratio, peak traffic, payload size, retention, and growth.
- Estimate requests per second, storage, bandwidth, and queue throughput before choosing infrastructure.

### Bottlenecks and scaling

- Check hot partitions/keys, database indexes and connection pools, cache miss rate, queue lag, and downstream rate limits.
- Distinguish horizontal scaling from removing a serial bottleneck or reducing work per request.
- Bound fan-out, page size, batch size, retries, and in-flight concurrency.

### Trade-offs and CAP

- Compare synchronous and asynchronous work, read and write amplification, strong and eventual consistency, and managed versus self-operated components.
- Under a network partition, state which operations favor consistency and which may remain available with stale or partial results.
- Describe the recovery path and how clients observe errors, delays, or degraded responses.

### Reliability and operations

- Use timeouts, bounded retries with jitter, idempotency, dead-letter handling, and backpressure where appropriate.
- Define cache fallback and invalidation behavior; durable storage remains the source of truth where required.
- Track p50/p95/p99 latency, error rate, saturation, cache hit ratio, queue lag, freshness, and dependency health.

## Timed Assessment

Complete a mixed DSA set, a Python review, a SQL review, and a timed LeetCode assessment. For each section, record correctness, elapsed time, the reason for any mistake, and one targeted follow-up exercise. Avoid counting an answer as mastered until you can explain the approach and complexity without notes.

## Portfolio Deliverable

Use [`System Design Portfolio Pack`](../projects/system-design-portfolio/README.md) as the index for the URL Shortener, Rate Limiter, Notification System, Chat Application, and News Feed designs. Before sharing the portfolio, verify that each artifact has requirements, a readable architecture, key flows, bottlenecks, explicit trade-offs, failure handling, and observability notes.
