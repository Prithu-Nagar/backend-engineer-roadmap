# Backend Architecture Review

Day 30 consolidates the backend architecture concepts covered during the
Backend Engineering phase.

## Architecture Review

A backend should be structured around clear responsibilities and boundaries.

```text
Client
  |
  v
API / Routing
  |
  v
Application / Service Layer
  |
  +--------> Domain / Business Rules
  |
  +--------> Repository / Data Access
                 |
                 v
              Database
```

Cross-cutting concerns such as authentication, validation, logging, testing,
and observability should be applied at appropriate boundaries rather than
embedded randomly inside business logic.

## Communication Choices

### Synchronous

```text
Client -> API -> Service -> Database -> Response
```

Use synchronous communication when the caller needs an immediate result and
the operation can reasonably complete within the request lifecycle.

### Asynchronous

```text
Client -> API -> Service -> Queue / Event Broker
                              |
                              +--> Worker
                              +--> Notification
                              +--> Analytics
```

Use asynchronous processing when work can be decoupled from the request path,
when consumers can process independently, or when buffering and retry behavior
are useful.

## Framework Boundary

The roadmap has used three Python backend approaches:

| Framework | Typical Strength | Main Consideration |
|---|---|---|
| Flask | Lightweight and flexible services | More components are selected separately |
| Django / DRF | Full-stack applications and REST APIs | Larger framework surface |
| FastAPI | Typed, API-focused, async-friendly services | Less full-stack functionality |

Framework choice should follow requirements rather than familiarity alone.

## Reliability Review

Important reliability boundaries include:

- Explicit timeout behavior
- Safe retries
- Idempotent operations
- Transaction boundaries
- Queue delivery semantics
- Backward-compatible schema changes
- Clear error responses
- Health and readiness checks

A retry should not automatically be applied to every failure. The operation
must be safe to repeat, and retry behavior should account for timeouts,
backoff, and duplicate work.

## Data and API Boundaries

The API contract and database schema evolve at different speeds. A safe
deployment strategy should allow old and new application versions to coexist
during rolling deployments.

```text
Old API instance ----                      +--> Compatible schema
New API instance ----/
```

Additive changes are generally easier to roll out than changes that immediately
remove or rename fields consumed by older instances.

## Review Checklist

Before approving a backend architecture, ask:

1. Are responsibilities separated clearly?
2. Is the chosen framework appropriate for the requirements?
3. Does each request have a clear path through the system?
4. Are synchronous and asynchronous boundaries intentional?
5. Are database transactions appropriately scoped?
6. Are retries and idempotency defined where needed?
7. Can old and new application versions coexist during deployment?
8. Are authentication, validation, logging, and observability placed at clear
   boundaries?
9. Can the system be tested without depending on external services?

## Day 30 Takeaway

The goal is not to maximize the number of architectural components. The goal
is to choose a simple structure that is easy to reason about today while
leaving deliberate boundaries for future scaling.
