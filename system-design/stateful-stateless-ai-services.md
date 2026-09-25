# Stateful vs Stateless AI Services

Day 56 compares stateful and stateless service designs for AI workloads,
especially when agents need conversation history, memory, and resumable
execution.

The key design decision is where conversational state lives and which
component owns it.

---

## Stateless AI Service

A stateless API instance does not keep durable conversation state in local
process memory.

```text
Client
  |
  v
Load Balancer
  |
  +----> AI API 1 ----+
  |                   |
  +----> AI API 2 ----+----> Session Store
  |                   |
  +----> AI API 3 ----+
```

Each request carries a session identifier, and the service retrieves the
required history from a shared durable store.

Advantages:

- Easy horizontal scaling
- Requests can reach any healthy instance
- Simpler failover
- Rolling deployments are easier
- Local memory does not become the source of truth

Trade-offs:

- Every request may require state retrieval
- Session-store latency becomes part of the request path
- The shared store must scale with traffic

---

## Stateful AI Service

A stateful service keeps active conversational state close to the serving
instance.

```text
Client
  |
  v
Session-aware Router
  |
  +----> AI Worker A ---> Local Session State
  |
  +----> AI Worker B ---> Local Session State
```

Advantages:

- Fast access to hot conversation state
- Potentially lower repeated state-fetch latency
- Useful for long-running workflows

Trade-offs:

- Routing becomes more complicated
- Instance failure can lose local state unless replicated
- Scaling and rebalancing are harder
- Deployments may need session-draining behavior

Stateful design does not remove the need for durable persistence when
conversation history must survive failures or restarts.

---

## Recommended State Boundary

A practical AI backend often keeps the HTTP/API tier stateless while storing
durable session state separately.

```text
                    +-------------------+
                    | Session Database  |
                    | + Context Store   |
                    +---------^---------+
                              |
Client -> Load Balancer -> AI API
                              |
                              v
                       Agent Runtime
                              |
                 +------------+------------+
                 |                         |
                 v                         v
              Tool APIs                 LLM API
```

The API instances can then scale horizontally without making local memory the
authoritative state store.

---

## Session State Layers

Not every piece of history needs to be sent to the model on every request.

A useful context model can separate:

1. **Recent messages**
   - Most recent user and assistant turns.
2. **Conversation summary**
   - Compressed representation of older history.
3. **Long-term memory**
   - Durable facts that are intentionally retained.
4. **Tool state**
   - Results or workflow state required to continue execution.
5. **Request context**
   - Tenant, user, permissions, locale, and other request-scoped data.

This separation helps control context size and keeps sensitive or irrelevant
data out of prompts.

---

## Context Loading Flow

```text
Incoming Request
      |
      v
Authenticate / Authorize
      |
      v
Load Session Metadata
      |
      +----> Recent Messages
      |
      +----> Conversation Summary
      |
      +----> Relevant Memory
      |
      +----> Active Tool / Workflow State
      |
      v
Context Builder
      |
      v
Agent Runtime
      |
      v
Response + State Updates
```

The context builder should apply explicit limits rather than loading an
unbounded conversation history.

---

## Failure Handling

Important failure scenarios include:

| Failure | Design consideration |
| --- | --- |
| API instance restart | Reload state from durable storage |
| Session store timeout | Apply bounded timeout and fallback |
| Duplicate request | Use idempotency or request identifiers |
| Concurrent session updates | Use versioning or optimistic locking |
| Context too large | Summarize or prune before model invocation |
| Tool execution failure | Persist failure state and allow controlled retry |

---

## Scaling Considerations

### Stateless API Tier

Scale API instances horizontally based on:

- Request rate
- Concurrent agent runs
- CPU / memory
- Model-provider latency

### Session Store

Scale the state layer based on:

- Active sessions
- Read/write operations
- Message volume
- Context snapshot size
- Retention requirements

### Agent Runtime

Agent execution can be separated from the request-serving tier when workflows
are long-running.

```text
API
 |
 +----> Agent Job Queue ----> Agent Workers
                                |
                                +----> Tools
                                |
                                +----> LLM
                                |
                                +----> Session Store
```

This avoids holding an HTTP request open for work that can be completed
asynchronously.

---

## Interview Questions

- Why is a stateless API tier often easier to scale?
- Where should durable conversation state live?
- When would a stateful worker be useful?
- How do you prevent concurrent updates from overwriting session state?
- How would you handle context windows that become too large?
- When should agent execution move to a background worker?
- What state is required to resume an interrupted agent workflow?
