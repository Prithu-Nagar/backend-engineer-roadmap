# Rate Limiter — HLD

## Day 66

Day 66 applies the HLD process to a Rate Limiter. The design focuses on a
shared decision service that can protect APIs while keeping latency predictable,
state bounded, and behavior explainable under distributed traffic.

---

## 1. Requirements

### Functional Requirements

- Allow or reject requests according to a configured rate limit.
- Support limits per user, API key, tenant, or IP where appropriate.
- Return a clear rejection response when a limit is exceeded.
- Expose remaining-limit and retry information to clients when the contract
  permits it.
- Support different policies for different endpoints or consumers.
- Allow policy changes without restarting every application instance.

### Non-Functional Requirements

- Low decision latency on the request path.
- Horizontally scalable across application instances.
- Predictable behavior during partial cache or datastore failure.
- Bounded memory usage and key cardinality.
- Observable accept/reject rates, latency, and policy behavior.

Non-goals for the first version:

- Perfect global ordering of requests across regions.
- Unlimited historical request storage.
- A complex policy language before the basic enforcement model is measured.

---

## 2. Core Algorithm

A token bucket is a useful default because it permits controlled bursts while
maintaining a long-term rate.

For a bucket with capacity `C` and refill rate `R` tokens/second:

```text
elapsed = now - last_refill
new_tokens = min(C, tokens + elapsed * R)

if new_tokens >= request_cost:
    tokens = new_tokens - request_cost
    allow
else:
    tokens = new_tokens
    reject
```

The state needs at least:

- Current token count.
- Last refill timestamp.
- Policy version or limit metadata when policies can change dynamically.

A fixed-window counter is simpler but can create boundary bursts. A sliding
window is more precise but generally requires more state. The choice should be
driven by product semantics and measured load.

---

## 3. Architecture

```text
                         +----------------+
Client ---------------->| API Gateway    |
                         +-------+--------+
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
             +-------------+           +-------------+
             | API Service |           | Rate Limit  |
             | instances   |---------->| Service     |
             +-------------+           +------+------+
                                             |
                                             v
                                       +-----------+
                                       | Redis     |
                                       | Cluster   |
                                       +-----------+
                                             |
                                             v
                                       Policy Store
```

The rate limiter can be embedded in the gateway for a simple deployment or
implemented as a shared service when multiple entry points need consistent
policy. The shared design avoids duplicating rate-limit state in every
application instance.

---

## 4. Request Flow

```text
Client
  |
  v
Gateway / API Service
  |
  +--> derive identity + policy key
  |
  +--> Rate Limiter
          |
          +--> atomic state update
          |
          +--> ALLOW ------> application handler
          |
          +--> REJECT -----> 429 response
```

The key should be deterministic, for example:

```text
rate:{policy_id}:{tenant_id}:{route_group}
```

Do not blindly use raw IP addresses when a stronger authenticated identity is
available. Key design also affects privacy, cardinality, and storage pressure.

---

## 5. Atomicity and Concurrency

Multiple application instances can evaluate the same bucket concurrently.
The state update therefore needs atomic semantics.

For Redis, a Lua script or equivalent server-side atomic operation can:

1. Read the current token state.
2. Calculate elapsed refill.
3. Decide whether the request is allowed.
4. Store the new token state.
5. Set or refresh the key TTL.
6. Return the decision and remaining capacity.

A sequence of independent `GET` and `SET` operations is unsafe because two
requests can both observe the same old token count.

---

## 6. Policy Model

A policy can be represented conceptually as:

| Field | Purpose |
|---|---|
| `policy_id` | Stable policy identifier |
| `scope` | user, tenant, key, route, or IP |
| `capacity` | Maximum bucket size |
| `refill_rate` | Tokens restored per second |
| `request_cost` | Tokens consumed by the operation |
| `enabled` | Allows controlled rollout/disablement |
| `version` | Supports policy changes |

Policy configuration should be separated from live counters. Changing a limit
should not require rewriting every active request counter manually.

---

## 7. Failure Modes

### Redis Unavailable

The system must choose an explicit fail-open or fail-closed policy.

- **Fail-open:** protects availability but can temporarily remove protection.
- **Fail-closed:** preserves the limit but can reject legitimate traffic.

A security-sensitive endpoint may prefer fail-closed, while a non-critical read
endpoint may prefer a bounded fail-open behavior. The decision belongs in the
service contract rather than being an accidental exception path.

### Hot Keys

A high-volume tenant or endpoint can concentrate traffic on one counter.
Mitigations include local pre-limits, careful policy grouping, and capacity
planning for the Redis cluster.

### Clock Differences

Distributed timestamps can produce inconsistent refill calculations. Prefer a
single authoritative time source at the stateful enforcement layer or use a
server-side datastore time primitive where available.

### Retry Storms

Clients retrying immediately after a 429 can amplify load. Return a sensible
`Retry-After` value and document client backoff behavior.

---

## 8. Consistency and Availability

A rate limiter usually needs strong enough consistency for a single policy key
during a short interval, but does not require globally perfect ordering.

For multi-region deployments, independent regional buckets improve latency and
availability but allow a user to exceed a nominal global limit by distributing
requests across regions. A globally coordinated limiter improves precision at
the cost of latency and cross-region dependency.

Choose the model from the product requirement:

- **Regional limit:** low latency and high availability.
- **Global limit:** stronger quota semantics with more coordination.

---

## 9. Capacity Planning

Estimate:

- Requests per second requiring a decision.
- Number of active rate-limit keys.
- Average key size.
- Policy lookup rate.
- Redis commands per decision.
- Peak versus average traffic.
- Replication and failover overhead.

The key-count estimate is especially important because a high-cardinality key
strategy can exhaust memory even when request throughput appears moderate.

---

## 10. Observability

Track:

- Allowed requests per policy.
- Rejected requests per policy.
- Rate-limit decision latency.
- Redis latency and error rate.
- Hot-key concentration.
- Active counter cardinality.
- Fail-open/fail-closed decisions.
- Policy version distribution.
- 429 response rate and retry behavior.

Logs should contain stable identifiers and decision metadata without exposing
unnecessary credentials or sensitive request content.

---

## 11. Interview Trade-offs

| Decision | Simpler Option | Scalable Option | Trade-off |
|---|---|---|---|
| Algorithm | Fixed window | Token bucket | Precision vs state/behavior |
| State | Local memory | Shared Redis | Consistency vs dependency |
| Deployment | Gateway plugin | Shared service | Simplicity vs reuse |
| Failure | Fail-open | Policy-specific behavior | Availability vs protection |
| Scope | IP only | Authenticated identity + route | Ease vs correctness |
| Regions | Regional | Globally coordinated | Latency vs quota precision |

The recommended starting point is a token-bucket policy backed by atomic Redis
state, with explicit failure behavior and measurements that can justify later
optimization.
