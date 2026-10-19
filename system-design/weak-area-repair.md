# Day 80 — System Design Weak-Area Repair

Use the Day 79 mock-interview scorecard to select one weak area. Do not redesign
the entire system; repair the specific gap and explain the trade-off.

## 1. Diagnose from evidence

Record a score from 1–5 and cite the point in the mock interview where the gap
appeared.

| Area | Score (1–5) | Evidence / unanswered question |
|---|---:|---|
| Requirements and API contracts |  |  |
| Capacity estimates and bottlenecks |  |  |
| Data model and access patterns |  |  |
| Caching and invalidation |  |  |
| Queues, retries, and idempotency |  |  |
| Availability and failure handling |  |  |
| Observability and operations |  |  |

## 2. Repair exercise

1. State functional and non-functional requirements.
2. Draw the request path and identify the component responsible for the gap.
3. Explain the expected load, data access pattern, and likely bottleneck.
4. Propose one focused change and at least one alternative.
5. Describe failure behavior, monitoring signals, and recovery.
6. Identify the cost, consistency, or operational trade-off.
7. Re-explain the design in five minutes without notes.

## 3. Self-check

- [ ] Requirements are explicit and testable.
- [ ] The bottleneck is supported by an estimate or observed evidence.
- [ ] The change addresses the root cause rather than masking symptoms.
- [ ] Failure modes and recovery behavior are described.
- [ ] Trade-offs and remaining limitations are acknowledged.
