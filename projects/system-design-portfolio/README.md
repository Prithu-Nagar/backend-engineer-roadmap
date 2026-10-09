# System Design Portfolio Pack

A concise interview-ready index of the system-design artifacts developed during Days 64–70. Each design records its main requirements, architecture, scaling choices, failure modes, and trade-offs. The designs are intentionally technology-aware without treating one implementation as universally correct.

## Portfolio Index

| System | Primary challenge | Main design decisions | Artifact |
|---|---|---|---|
| URL Shortener | High-volume redirects and key generation | Stable short codes, redirect caching, durable mappings, abuse controls | [`URL Shortener deep dive`](../../system-design/url-shortener-deep-dive.md) |
| Rate Limiter | Consistent request admission under concurrency | Token bucket, atomic shared state, deterministic keys, explicit failure policy | [`Rate Limiter HLD`](../../system-design/rate-limiter-hld.md) |
| Notification System | Reliable multi-channel delivery | Transactional outbox, durable queue, isolated workers, retries and dead letters | [`Notification System HLD`](../../system-design/notification-system-hld.md) |
| Chat Application | Real-time delivery with durable history | WebSocket gateways, shared message storage, cross-instance fan-out, reconnect recovery | [`Chat Application HLD`](../../system-design/chat-application-hld.md) |
| News Feed | Fast personalized reads at high fan-out | Hybrid fan-out, cursor pagination, bounded cache, asynchronous materialization | [`News Feed HLD`](../../system-design/news-feed-hld.md) |

## Review Framework

For each design, be ready to explain the following in order:

1. **Requirements:** Clarify users, core use cases, scale, latency targets, durability, and consistency expectations.
2. **API and data model:** Define request/response contracts, identifiers, indexes, retention, and idempotency requirements.
3. **Capacity:** Estimate requests per second, storage growth, bandwidth, cache size, and queue throughput using stated assumptions.
4. **Architecture:** Trace the read and write paths; identify synchronous calls, asynchronous work, and ownership boundaries.
5. **Bottlenecks:** Find hot keys, high-fan-out users, database contention, queue lag, connection limits, and expensive cache misses.
6. **Trade-offs:** Compare at least two plausible options and state the workload or requirement that would justify each.
7. **Reliability:** Discuss timeouts, retries with jitter, idempotency, overload controls, fallback behavior, and recovery.
8. **Observability and security:** Name the metrics, logs, traces, access controls, abuse protections, and sensitive-data boundaries.

## Bottleneck and Trade-off Checklist

- [ ] Identify the expected bottleneck at current scale and the next likely bottleneck as traffic grows.
- [ ] Separate throughput, latency, availability, consistency, and durability requirements.
- [ ] Explain cache TTL, invalidation, stampede protection, and durable-source fallback.
- [ ] Bound queues, batches, pagination sizes, retries, and concurrent work.
- [ ] State whether duplicate requests/events are safe and how idempotency is enforced.
- [ ] Explain how partitions, replicas, and regional deployment affect ordering and consistency.
- [ ] Describe graceful degradation when Redis, a broker, a downstream provider, or a region fails.
- [ ] Define actionable SLOs and alert signals, including queue lag and tail latency.

## CAP Theorem: Interview Notes

During a network partition, a distributed data system must make a practical choice between consistency and availability for the affected operation. CAP is not a blanket label for an entire application: different operations and data stores may make different choices. State the partition scenario, the consistency guarantee required by the operation, and the user-visible behavior when the system cannot satisfy both consistency and availability. Do not confuse CAP with the routine latency trade-off described by PACELC.

## Timed Review Exercise

Set a 45-minute timer and select one system from the index:

- 5 minutes: clarify requirements and assumptions.
- 5 minutes: estimate capacity and identify data entities.
- 10 minutes: draw the high-level architecture and API/data flow.
- 10 minutes: identify two bottlenecks and compare design alternatives.
- 10 minutes: cover failure modes, consistency, and recovery.
- 5 minutes: summarize trade-offs and metrics without looking at notes.

Record the weakest section and revisit the corresponding design artifact. Keep estimates explicit and approximate; explain assumptions rather than presenting guesses as facts.
