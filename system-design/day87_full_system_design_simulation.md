# Day 87 — Full System Design Simulation

## Exercise

Conduct one end-to-end design interview for a multi-tenant Task Manager API. Aim for 45–60 minutes and narrate decisions rather than jumping directly to components.

## Interview sequence

1. **Requirements (5 min):** define task creation, listing, updates, deletion, ownership, pagination, and availability expectations.
2. **Scale and constraints (5 min):** estimate active users, request rate, data growth, read/write ratio, and retention. State assumptions explicitly.
3. **API and data model (10 min):** define endpoints, status codes, task ownership, indexes, uniqueness/integrity rules, and pagination contract.
4. **Architecture (10 min):** explain edge/API layer, application services, repository, relational database, cache, background workers, and observability.
5. **Reliability and security (10 min):** cover timeouts, bounded retries, rate limits, authentication, per-resource authorization, backups, and recovery.
6. **Trade-offs (5–10 min):** identify bottlenecks, consistency needs, cache invalidation, and when additional infrastructure is justified.

## Capacity-estimation prompts

- What is the expected average and peak request rate?
- How much data is written daily and retained over one year?
- Which queries need indexes, and what is the write cost?
- What cache hit rate would materially reduce database load?
- Which operations are safe to retry, and how will duplicate writes be prevented?

Use estimates as assumptions, not measured facts. Show units and arithmetic.

## Failure-mode review

| Failure | Response | Signal |
|---|---|---|
| Database saturation | Apply timeouts, shed noncritical load, investigate pool/query latency | Pool wait, query latency, error rate |
| Cache unavailable | Fall back only if database capacity permits; bound extra load | Cache errors and database load |
| Worker backlog | Apply backpressure and alert on age/depth | Queue depth and oldest-message age |
| Duplicate request | Use idempotency where the operation requires it | Duplicate-key conflicts |
| Cross-tenant access attempt | Deny access at the data/service boundary | Authorization-denial audit event |

## Evaluation checklist

- [ ] Requirements and nonfunctional goals are explicit.
- [ ] API contracts and data ownership are consistent.
- [ ] Capacity assumptions and bottlenecks are reasoned through.
- [ ] Security and failure modes are addressed.
- [ ] Trade-offs are explained, including what is intentionally not built.
- [ ] Observability and recovery are part of the design.
