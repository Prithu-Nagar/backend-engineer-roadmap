# Rate Limiter — Mock System Design Interview

Use this artifact for a 35–45 minute interview. State assumptions, compare algorithms, and explain behavior during dependency failures.

## 1. Clarify Requirements

Functional requirements:
- Limit requests by a defined key such as user, API key, IP, tenant, or endpoint.
- Support configurable limits and windows, with clear responses when a limit is exceeded.
- Provide policy overrides for trusted clients and different API tiers where needed.

Non-functional requirements:
- Low latency and high throughput on the request path.
- Consistent enough enforcement for the product's abuse and fairness goals.
- Safe behavior during cache/network failures and configuration changes.
- Observable decisions without collecting unnecessary personal data.

Clarify whether limits are strict or approximate, whether bursts are allowed, and whether the service must coordinate across regions.

## 2. Estimate Capacity

Choose illustrative assumptions rather than presenting them as facts. For example, at 50,000 incoming requests per second, the limiter must sustain that decision rate plus replication and operational overhead. Estimate active keys from distinct clients in the window, memory per key, key churn, and the cost of atomic updates. Separate steady-state traffic from bursts and hot-key behavior.

## 3. Compare Algorithms

- **Fixed window counter:** simple and memory-efficient, but permits boundary bursts.
- **Sliding log:** accurate timestamps per request, but can be expensive in memory and operations.
- **Sliding window counter:** approximates a rolling window with lower storage overhead.
- **Token bucket:** permits controlled bursts while enforcing a long-term rate.
- **Leaky bucket:** smooths output rate, useful when steady processing matters.

Select based on semantics, memory, latency, and how much approximation is acceptable.

## 4. API and Decision Contract

A limiter can expose an internal decision operation such as `check_and_consume(key, policy, cost) -> decision`. Return allow/deny, remaining capacity when meaningful, and a retry hint when it can be computed safely. For HTTP APIs, `429 Too Many Requests` and a documented `Retry-After` policy are common. Ensure updates are atomic for the chosen algorithm.

## 5. High-Level Architecture

1. An API gateway or middleware derives a trusted client identity.
2. Policy configuration resolves the applicable limit and algorithm.
3. A limiter service or shared store performs an atomic check/update.
4. The request proceeds or receives a rate-limit response.
5. Metrics and sampled decision events feed dashboards and alerts.
6. Policy changes are versioned and propagated with bounded delay.

Do not blindly trust client-supplied forwarding headers; configure trusted proxies and identity derivation explicitly.

## 6. Distributed Consistency and Failure Modes

- Atomic scripts or transactions can coordinate counters within a shared store, but hot keys and cross-region latency remain concerns.
- Local in-memory limits are fast but may over-admit across instances.
- Partitioning by key distributes load but can create hot partitions.
- During store failure, choose fail-open or fail-closed by endpoint risk; consider bounded local fallback limits rather than a universal rule.
- Define behavior for clock skew, TTL expiry, policy rollout, retries, and duplicated requests.

## 7. Security and Observability

- Protect the limiter from key-cardinality attacks and unbounded client-controlled keys.
- Avoid relying solely on IP addresses when NAT or proxying changes identity semantics.
- Track allow/deny rate, decision latency, store errors, hot keys, policy version, and fallback activations.
- Avoid logging raw API keys or personal identifiers; use controlled, privacy-aware aggregation.

## Follow-up Questions

1. How would you implement a token bucket atomically in Redis?
2. What happens when many clients share one NAT address?
3. How would you enforce a tenant-wide quota across multiple API instances?
4. When would you choose fail-open versus fail-closed?
5. How would you avoid a thundering herd after a policy update?
6. How do multi-region deployments trade strictness for latency and availability?

## Interview Evaluation Checklist

- [ ] Clarified identity, burst, window, and consistency requirements.
- [ ] Compared at least three algorithms and justified the selection.
- [ ] Explained atomicity, key distribution, and hot-key behavior.
- [ ] Defined 429 behavior and retry semantics.
- [ ] Covered failure policy, abuse resistance, and observability.
