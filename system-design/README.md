# System Design

This directory contains system design concepts relevant to backend engineering, scalable applications, distributed systems, and production architecture.

The focus is on understanding how backend systems are structured, how components communicate, and how systems scale as traffic and data grow.

---

## Topics Covered

- Monolith vs Microservices
- Reverse Proxy
- Load Balancing
- Caching
- Database Scaling
- Redis
- Authentication & Authorization
- API Gateway
- Rate Limiting
- Idempotency
- Message Queues

---

## Monolith vs Microservices

Covers the architectural differences between monolithic and microservice-based systems.

Topics include:

- Monolithic architecture
- Microservices architecture
- Service boundaries
- Independent deployment
- Scalability
- Operational complexity

File: `monolith_vs_microservices.md`

---

## Reverse Proxy

Covers the role of reverse proxies between clients and backend services.

Topics include:

- Request forwarding
- TLS termination
- Load balancing
- Security
- Routing

File: `reverse_proxy.md`

---

## Load Balancing

Covers distributing incoming requests across multiple backend instances.

Topics include:

- Horizontal scaling
- Load-balancing algorithms
- Health checks
- Availability
- Fault tolerance

File: `load_balancer.md`

---

## Caching

Covers using caches to reduce latency and database load.

Topics include:

- Cache-aside
- Read-through caching
- Write-through caching
- Cache invalidation
- TTL
- Cache consistency

File: `caching.md`

---

## Database Scaling

Covers approaches for scaling databases as traffic and data volume increase.

Topics include:

- Vertical scaling
- Horizontal scaling
- Read replicas
- Database partitioning
- Sharding
- Replication
- Connection management

File: `database-scaling.md`

---

## Redis

Covers Redis as an in-memory data store commonly used for caching and other backend use cases.

Topics include:

- Key-value storage
- Caching
- TTL
- Sessions
- Counters
- Distributed locks

File: `redis.md`

---

## Authentication & Authorization

Authentication establishes the identity of a user, while authorization determines what that user is allowed to access.

Topics include:

- Authentication vs authorization
- Session-based authentication
- Token-based authentication
- Password hashing
- Access control
- Least privilege
- Secure credential handling
- Authentication architecture
- Authorization checks

File: `authentication-authorization.md`

---

## API Gateway

An API Gateway acts as a centralized entry point for clients communicating with backend services.

It can handle common API-level concerns such as:

- Request routing
- Authentication
- Rate limiting
- Request validation
- Logging
- Monitoring
- API versioning
- Request transformation

Example:

Client
   |
   v
API Gateway
   |
```text
   +----> User Service
```
   |
```text
   +----> Task Service
```
   |
```text
   +----> Order Service

```
The client does not need to know the internal topology of the backend services.

API Gateway Responsibilities
Request Routing

The gateway determines which backend service should process a request.

GET /users
    |
    v
API Gateway
    |
    v
User Service
GET /tasks
    |
    v
API Gateway
    |
    v
Task Service
Authentication

The gateway can validate authentication credentials or tokens before forwarding requests.

However, services should still enforce authorization for resources they own.

## Rate Limiting

Covers controlling request frequency to protect backend services.

Topics include:

- Fixed Window
- Sliding Window
- Token Bucket
- Leaky Bucket
- HTTP 429
- Distributed Rate Limiting
- Redis-based rate limiting
- API Gateway rate limiting

File: `rate_limiting.md`

The gateway can restrict how many requests a client can make within a given period.

Example:

100 requests per minute per user

When the limit is exceeded:

Client
   |
   v
API Gateway
   |
   v
429 Too Many Requests
Observability

The gateway is a useful location for collecting:

Request counts
Response times
Error rates
Access logs
Trace IDs
API Gateway vs Reverse Proxy

A reverse proxy forwards requests to backend servers.

An API Gateway can provide reverse-proxy functionality while also handling API-specific concerns such as:

Authentication
Rate limiting
API routing
API versioning
Request transformation
Observability
API Gateway vs Load Balancer

A load balancer primarily distributes traffic across backend instances.

An API Gateway focuses on API-level concerns.

They can also be used together:

Client
   |
   v
API Gateway
   |
   v
Load Balancer
   |
```text
   +----> Service 1
```
   |
```text
   +----> Service 2
```
   |
```text
   +----> Service 3
```
High Availability

The API Gateway can become a critical component of the architecture.

A single gateway instance can become a single point of failure.

Multiple gateway instances can improve availability:

             Client
                |
                v
          Load Balancer
           /          \
          v            v
     Gateway 1    Gateway 2
          \            /
           \          /
            v        v
              Services
Business Logic

Business logic should generally remain inside backend services rather than the API Gateway.

Prefer:

API Gateway
    |
```text
    +----> Routing
```
    |
```text
    +----> Authentication
```
    |
```text
    +----> Rate Limiting
```
    |
```text
    +----> Observability
```
    |
    v
Backend Services
    |
```text
    +----> Business Logic
```
    |
```text
    +----> Data Access
```
Revision Summary
Client
    |
    v
API Gateway
    |
```text
    +----> Authentication
```
    |
```text
    +----> Rate Limiting
```
    |
```text
    +----> Routing
```
    |
```text
    +----> Observability
```
    |
    v
Backend Services

Remember:

```text
Reverse Proxy
→ Forwards traffic

Load Balancer
→ Distributes traffic

API Gateway
→ Central API entry point and API-level cross-cutting concerns

```
---

### Resilience

Day 18 introduces resilience patterns for distributed backend systems.

Topics include:

- Timeouts
- Retries
- Exponential backoff
- Retryable failures
- Non-retryable failures
- Idempotency
- Idempotency keys

The goal is to prevent slow or failing dependencies from causing
cascading failures and unintended duplicate operations.

---

## Idempotency — Day 19

Day 19 introduces idempotency for reliable distributed APIs.

Topics include:

- Idempotency
- Idempotency keys
- Duplicate request handling
- Request hashing
- Retry-safe APIs
- Idempotency storage
- Concurrent duplicate requests
- Payment/order retry scenarios

File:

`idempotency.md`

Idempotency is particularly important for operations such as payments,
orders, job creation, and other requests where repeating the operation
could

---

## Database-per-Service — Day 22

Database-per-service is a microservice architecture pattern where each
service owns its data store and controls access to its own schema.

File:

`database-per-service.md`

Core principle:

```text
Service A ──> Database A
Service B ──> Database B
Service C ──> Database C
```

A service should not directly read or modify another service's database.

### Benefits

- Strong service ownership
- Independent schema evolution
- Reduced coupling between services
- Independent scaling decisions
- Clearer domain boundaries

### Trade-offs

- Cross-service queries become harder
- Distributed transactions may be required
- Data duplication can become necessary
- Eventual consistency may need to be handled explicitly

Database-per-service is most useful when service boundaries are sufficiently
clear and independent ownership provides more value than a shared database.

---

# System Design Approach

For each system design topic:

1. Understand the problem.
2. Identify functional requirements.
3. Identify non-functional requirements.
4. Define the major system components.
5. Understand data flow between components.
6. Identify scalability and reliability concerns.
7. Consider failure scenarios.
8. Evaluate architectural trade-offs.

The goal is to understand why a particular architecture is appropriate rather than memorizing a single system design.

---

## Learning Progress

|             Topic              |  Status   |
|--------------------------------|-----------|
| Monolith vs Microservices      | Completed |
| Reverse Proxy                  | Completed |
| Load Balancing                 | Completed |
| Caching                        | Completed |
| Database Scaling               | Completed |
| Redis                          | Completed |
| Authentication & Authorization | Completed |
| API Gateway                    | Completed |
| Rate Limiting                  | Completed |
| Message Queues                 | Completed |

---

## Upcoming Topics

- Kafka
- Distributed Systems
- Message Queues
- Event-Driven Architecture

---

## Service Communication — Day 23

Day 23 compares synchronous REST communication with asynchronous messaging.

File:

`service-communication.md`

The key decision is whether the caller needs an immediate response or whether
the work can be decoupled and processed asynchronously.

REST is useful for direct request/response interactions, while asynchronous
messaging is useful for background work, event-driven workflows, and buffering
traffic between services.

---

## Day 24 — Synchronous vs Asynchronous Workflows

Day 24 focuses on choosing between work that completes inside the request path
and work that continues asynchronously.

File:

`synchronous-vs-asynchronous-workflows.md`

Topics include:

- Request/response latency
- Background processing
- Queues and workers
- Failure isolation
- Eventual consistency
- Retry and idempotency considerations
- Choosing the simplest workflow that satisfies the requirement

## Message Queues

Day 25 introduces message queues and the reasons backend systems use them.

Topics include:

- Synchronous vs asynchronous workflows
- Producer/consumer architecture
- At-least-once delivery
- Retries and dead-letter queues
- Idempotent consumers
- Ordering and operational trade-offs
- Queue monitoring

File: `message_queues.md`

---

## Day 26 — Queue Semantics & At-Least-Once Delivery

Day 26 extends the message-queue concepts introduced on Day 25 by focusing on
delivery semantics and the implications for backend consumers.

Topics include:

- At-least-once delivery
- Duplicate message handling
- Idempotent consumers
- Retry behavior
- Dead-letter queues
- Ordering boundaries
- Queue depth and processing-latency monitoring

File:

`message_queues.md`

The existing Day 25 queue material is retained and expanded with the Day 26
semantics focus.

---

## Day 27 — Event-Driven Architecture

Day 27 introduces event-driven architecture and the use of events to decouple
producers from consumers.

Topics include:

- Events vs commands
- Producers and consumers
- Event brokers/topics
- Fan-out
- Asynchronous processing
- Eventual consistency
- Idempotent consumers
- Event schema versioning
- Retry and dead-letter handling
- Ordering and observability

File:

`event-driven-architecture.md`

Event-driven architecture is useful when multiple components react to business
events or when asynchronous processing reduces coupling, but it introduces
additional distributed-system complexity.

---

## Day 28 — Event-Driven Architecture Trade-Offs

Day 28 revisits event-driven architecture as an architecture decision rather
than treating asynchronous events as a default.

Topics include:

- Synchronous vs event-driven communication
- Latency and eventual consistency trade-offs
- Queue vs event-stream considerations
- Independent consumer scaling
- Event schema evolution
- Duplicate delivery and idempotency
- Observability and distributed debugging
- Decision checklist for introducing events

File:

`event-driven-architecture.md`

The goal is to choose event-driven communication when its decoupling and
asynchronous benefits justify the additional distributed-system complexity.

---

## Day 29 — Schema Evolution

Day 29 focuses on evolving database and API schemas without breaking existing
consumers or older application instances during deployment.

Topics include:

- Expand-and-contract migrations
- Backward compatibility
- Rolling deployments
- Additive API changes
- Safe data backfills
- Deprecation and contract phases
- Schema compatibility testing

File:

`schema_evolution.md`

The goal is to make schema changes incremental so deployment timing does not
become a correctness dependency.

---

## Day 30 — Backend Architecture Review

Day 30 consolidates the backend architecture concepts introduced during the
Backend Engineering phase.

Review areas:

- Layered backend architecture
- API and service boundaries
- Synchronous vs asynchronous communication
- Message queues and delivery semantics
- Event-driven architecture
- Schema evolution and backward compatibility
- Authentication and authorization boundaries
- Caching and database interaction
- Testing and observability boundaries

Detailed review:

`backend-architecture-review.md`

The objective is to select the simplest architecture that satisfies the
requirements while making reliability, scalability, and operational trade-offs
explicit.

---

## Day 31 — Database Connection Pooling & Saturation

Day 31 introduces connection pooling as a capacity-management problem between
application instances and a relational database.

Topics include:

- Connection reuse
- Bounded pool capacity
- Pool saturation
- Connection acquisition and release
- Pool sizing with horizontal scaling
- Connection leaks
- Long-running transactions
- Database capacity limits
- Pool health metrics

Detailed notes:

`database-connection-pooling.md`

The focus is on understanding that increasing pool size is not equivalent to
increasing database throughput.

---

## Day 32 — Distributed Locks

Day 32 introduces distributed locks as a coordination mechanism for work that
can be executed by multiple application instances.

Topics include:

- Distributed lock scope
- Local locks vs distributed locks
- Lock ownership
- Lease / TTL concepts
- Worker failure scenarios
- Database locks vs distributed locks
- Idempotency and failure handling

Detailed notes:

`distributed-locks.md`

The focus is on defining the critical section and failure model before choosing
a coordination mechanism.

---

## Day 33 — Worker Queues

Day 33 introduces worker queues for asynchronous backend processing.

Topics include:

- Producer/consumer architecture
- Moving work out of the request path
- At-least-once delivery considerations
- Retries and dead-letter handling
- Ordering requirements
- Worker scaling
- Queue depth and job-age monitoring
- In-process tasks vs durable external queues

Detailed notes:

`worker-queues.md`

The focus is on defining delivery, failure, idempotency, and capacity
requirements before choosing a queue implementation.

---

## Day 34 — Database Partitioning & Sharding

Day 34 focuses on partitioning and sharding as database scaling techniques.

Topics include:

- Partitioning vs sharding
- Range, list, and hash partitioning
- Partition-key selection
- Partition pruning
- Shard routing
- Hot partitions and hot shards
- Cross-partition and cross-shard queries
- Rebalancing and operational considerations

Detailed notes:

`database-partitioning.md`

The focus is on introducing partitioning or sharding only when measured data
volume, query patterns, or capacity requirements justify the added complexity.

---

## Day 35 — Read Replicas & Replication Lag

Day 35 focuses on scaling read-heavy workloads with database read replicas.

Topics include:

- Primary and replica roles
- Read/write splitting
- Replication lag
- Read-after-write consistency
- Replica health and routing
- Fallback to the primary
- Replica capacity and monitoring

Detailed notes:

`read-replicas.md`

The focus is on making consistency requirements explicit before routing traffic
to replicas and on treating replication lag as an operational signal.

---

## Day 36 — Cache Invalidation, TTL & Cache Stampede

Day 36 focuses on the consistency and reliability concerns introduced by
shared caching.

Topics include:

- Cache-aside
- Cache invalidation
- TTL
- Redis key design
- Cache stampede
- Request coalescing
- TTL jitter
- Stale-while-revalidate
- Cache failure and database fallback

Detailed notes:

`cache-invalidation.md`

The focus is on treating caching as an optimization while explicitly designing
for stale data, expiration bursts, cache outages, and database load.

---

## Day 37 — Distributed Tracing

Day 37 introduces distributed tracing as an observability mechanism for
following requests across service boundaries.

Topics include:

- Traces and spans
- Trace IDs and span IDs
- Parent/child relationships
- Trace-context propagation
- Sampling
- Instrumentation boundaries
- Logs, metrics, and traces

Detailed notes:

`distributed-tracing.md`

The focus is on connecting application logs, database activity, and
distributed request paths so latency and failures can be investigated
end-to-end.

---

## Day 38 — Retries, Exponential Backoff & Jitter

Day 38 focuses on controlled recovery from transient failures in distributed
systems.

Topics include:

- Retryable vs non-retryable failures
- Exponential backoff
- Jitter
- Retry budgets
- Deadlines
- Idempotency
- Retry storms
- `Retry-After`

Detailed notes:

`retries.md`

The focus is on making retries bounded and deliberate so recovery mechanisms do
not amplify an outage.

---

## Day 39 — Circuit Breakers & Bulkheads

Day 39 focuses on containing dependency failures and protecting service
capacity during partial outages.

Topics include:

- Circuit breaker pattern
- Closed, open, and half-open states
- Fail-fast behavior
- Bulkheads
- Worker and connection-pool isolation
- Concurrency limits
- Retry and circuit-breaker interaction
- Capacity and resilience metrics

Detailed notes:

`circuit-breakers-bulkheads.md`

The focus is on preventing cascading failures by limiting both dependency calls
and resource consumption.

---

## Day 40 — Distributed Systems Review

Day 40 consolidates the distributed-systems concepts introduced during Days
31–39 before the roadmap moves into Production Engineering.

Review areas:

- Database scaling, partitioning, and replication
- Read replicas and replication lag
- Connection pooling
- Background workers and queues
- Caching and cache invalidation
- Retries, backoff, and jitter
- Circuit breakers and bulkheads
- Distributed tracing and observability
- Reliability, failure isolation, and capacity trade-offs

The review emphasizes identifying bottlenecks and failure modes, then selecting
an appropriate distributed-systems pattern rather than applying patterns in
isolation.

---

## Day 41 — Containerized Service Architecture

Day 41 introduces containerization as a deployment and scaling boundary for
backend services.

Topics include:

- Images vs containers
- Stateless application containers
- Containerized service architecture
- Externalizing durable state
- Resource boundaries
- Container failure models
- Dockerfile responsibilities
- Production containerization checklist

Detailed notes:

`containerized-service-architecture.md`

Docker Compose and multi-container local orchestration are intentionally
covered on Day 42.

---

## Day 42 — Local Distributed Environment

Day 42 models a local distributed environment with independently running
application, database, and cache containers.

Topics include:

- Multi-container architecture
- Service discovery through Compose service names
- Health checks
- Persistent state
- Independent container failure
- Dependency boundaries
- Local orchestration vs production orchestration

Detailed notes:

`local-distributed-environment.md`

The repository root `docker-compose.yml` provides the concrete local
environment.

---

## Day 43 — Production Engineering

Day 43 introduces CI/CD as an automated architecture boundary.

Topics include:

- CI vs CD
- Pipeline stages
- Quality gates
- Artifact flow
- Deployment and health-check boundaries

Detailed notes:

`cicd-pipeline.md`

---

## Day 44 — Deployment Strategies

Day 44 reviews deployment approaches for introducing new backend versions safely.

Topics include:

- Rolling deployments
- Blue/green deployments
- Canary deployments
- Rollback considerations
- Version compatibility
- Expand-and-contract database changes

Detailed notes:

`deployment-strategies.md`

---

## Day 45 — Reverse Proxy + Application Servers

Day 45 connects deployment fundamentals with the production request path.

Topics include:

- Reverse proxy responsibilities
- WSGI application servers
- ASGI application servers
- TLS termination
- Upstream routing and timeouts
- Graceful shutdown and stateless application instances

Detailed notes:

`reverse-proxy-app-server.md`

---

## Day 46 — Observability

Day 46 covers observability as a production system capability.

Topics include:

- Structured logs
- Metrics and latency percentiles
- Distributed traces
- Correlation IDs
- Liveness versus readiness
- Dashboards and actionable alerts
- Connecting logs, metrics, and traces during incidents

Detailed notes:

`observability.md`

---

## Day 47 — Security Boundaries & Threat Modeling

Day 47 models security as a system-design concern rather than only an
application-code concern.

Topics include:

- Trust and security boundaries
- Threat-modeling questions
- Spoofing
- Tampering
- Information disclosure
- Denial of service
- Authentication and authorization boundaries
- Least privilege
- Secret management and safe logging

Detailed notes:

`security-boundaries-threat-modeling.md`

---

## Day 48 — Secrets Management

Day 48 models secrets as an operational system-design concern.

Topics include:

- Runtime secret injection
- Environment variables versus managed secret stores
- Service-specific secret access
- Secret rotation
- Secret revocation
- Auditing access without logging secret values
- Keeping credentials outside source control and container images

Detailed notes:

`secrets-management.md`

---

## Day 49 — Failure Scenarios & Recovery

Day 49 models production failure handling as a system-design workflow.

Topics include:

- Application, database, and dependency failure scenarios
- Rollback decision criteria
- Recovery/degraded modes
- Failure containment
- Incident detection, assessment, mitigation, recovery, and review

Detailed notes:

`failure-scenarios-and-runbook.md`

---

## Day 50 — Production Readiness Review

Day 50 consolidates the system-design concerns required for production-ready
services.

Review areas:

- Containerized service architecture
- CI/CD and deployment strategies
- Reverse proxies and application servers
- Observability and health checks
- Security boundaries and secrets management
- Dependency failures and incident response
- Rollback and recovery modes
- Caching, queues, retries, and resilience
- Bottleneck and failure-mode analysis

The review emphasizes connecting reliability, security, deployment, observability,
and recovery decisions into one production-readiness perspective.

---

## Day 51 — AI-Enabled Backend Architecture

Day 51 introduces system-design boundaries for adding LLM capabilities to an
existing backend.

Topics include:

- API and authentication boundaries
- Application-service orchestration
- Prompt/model/parser separation
- External LLM dependency handling
- Timeouts, retries, rate limits, and failure modes
- Output validation
- AI-specific observability and cost tracking

Detailed notes:

`ai-enabled-backend-architecture.md`

The design keeps AI orchestration inside explicit service boundaries while
leaving authentication, business rules, reliability, and operational controls
with the backend.

---

## Day 52 — Streaming Architecture

Day 52 introduces architecture patterns for incrementally delivering backend
and AI responses.

Topics include:

- HTTP streaming
- Server-Sent Events (SSE)
- WebSockets and when bidirectional communication is required
- Backpressure and bounded buffering
- Client disconnects and cancellation
- Long-lived connection scaling
- Streaming observability

Detailed notes:

`streaming-architecture.md`

---

## Day 53 — RAG System Architecture

Day 53 covers the online architecture of a Retrieval-Augmented Generation
system.

Topics include:

- Query validation and normalization
- Metadata and tenant filtering
- Vector and keyword retrieval
- Candidate reranking
- Context construction
- LLM integration boundaries
- Reliability, scaling, and observability
- Retrieval and answer-quality evaluation signals

Detailed notes:

`rag-system-architecture.md`

---

## Day 54 — Offline Ingestion vs Online Serving

Day 54 separates the asynchronous RAG ingestion workload from the
latency-sensitive online serving path.

Topics include:

- Offline parsing, chunking, embedding, and indexing
- Online query, retrieval, reranking, and generation
- Queue-backed ingestion workers
- Idempotency and job metadata
- Document and embedding versioning
- Independent scaling and failure handling
- Last-known-good index serving during ingestion failures

Detailed notes:

`offline-ingestion-online-serving.md`

The architecture gives ingestion and serving different scaling, reliability,
and latency boundaries while keeping their data contracts explicit.

---

## Day 55 — Agent Architecture

Covers the architecture of AI agents that plan work, call bounded tools,
maintain state, and enforce application-level guardrails.

Topics include:

- Agent orchestration
- Tool registries
- Agent state
- Planning
- Guardrails
- Failure handling
- Stateful vs stateless agent services
- Agent observability

File: `agent-architecture.md`

---

## Day 56 — Stateful vs Stateless AI Services

Day 56 compares service architectures for AI applications that maintain
conversation and workflow state.

Topics include:

- Stateless API tiers
- Stateful workers
- Shared session stores
- Context loading
- Long-running agent execution
- Horizontal scaling
- Failure recovery
- Session consistency

File:

`stateful-stateless-ai-services.md`

The design emphasizes keeping durable state outside horizontally scaled API
instances when stateless request handling is preferred, while using stateful
workers selectively for long-running workflows.

---

## Day 57 — Tool / Resource Boundary Design

Day 57 defines how an MCP-style protocol boundary can expose application
capabilities without granting unrestricted access to internal systems.

Topics include:

- Tool boundaries
- Resource boundaries
- Authorization
- Tenant isolation
- Reliability controls
- Observability
- Stateless scaling
- Long-running tool execution

File:

`tool-resource-boundary-design.md`

The design treats tools and resources as explicit application capabilities with
clear schemas, permissions, and operational boundaries.

---

## Day 58 — AI Reliability and Fallback Strategies

Day 58 covers reliability patterns for AI-backed services.

Topics include:

- Dependency timeouts
- Bounded retries and backoff
- Circuit breakers
- Model and dependency fallbacks
- Graceful degradation
- Latency budgets
- Stable client-facing error categories
- Preserving authorization and tenant boundaries during fallback

File:

`ai-reliability-fallbacks.md`

The design treats fallback behavior as an explicit reliability policy rather
than silently hiding dependency failures.

---

## Day 59 — AI Cost / Performance Architecture

Day 59 designs an AI-backed service around explicit cost, latency, throughput,
and reliability controls.

Topics include:

- Model-selection policy
- Token and context budgeting
- Caching
- Rate limits and tenant quotas
- Latency budgets
- Retry/fallback cost
- Usage and cost observability
- Capacity planning across requests, tokens, and spend

File:

`ai-cost-performance-architecture.md`

The design treats cost and performance as first-class service concerns while
preserving authorization, tenant isolation, and reliability boundaries.

---

## Day 60 — AI Architecture Review

Day 60 consolidates the system-design patterns developed for AI-backed services.

Review areas:

- AI dependency and provider boundaries
- Stateful versus stateless AI services
- RAG ingestion and online serving separation
- Tool and resource authorization boundaries
- Streaming and backpressure
- Reliability, timeouts, retries, and fallbacks
- Rate limits, quotas, caching, and token budgets
- Cost, latency, throughput, and capacity planning
- Observability and tenant isolation

The review focuses on connecting requirements, failure modes, scaling decisions,
and operational controls into a coherent AI-service architecture.

---

## Day 61 — LLD: SOLID, Composition, and Interfaces

Day 61 begins the System Design & LLD phase with reusable object-design
principles for scalable backend services.

Topics include:

- SOLID principles
- Composition over inheritance
- Small interfaces and dependency inversion
- Presentation, application, domain, and infrastructure boundaries
- Transaction and authorization boundaries
- Repository and external-service abstractions
- Trade-offs of adding abstraction to small services

File:

`lld-principles-solid-composition-interfaces.md`

The design keeps concrete infrastructure at the edge while application policy
depends on stable contracts.

---

## Day 62 — LLD: Factory and Strategy Patterns

Day 62 extends the LLD phase with two patterns for controlled object creation
and interchangeable behavior.

Topics include:

- Factory as a composition/creation boundary
- Strategy as an interchangeable business-rule boundary
- Combining Factory + Strategy without coupling application policy to concrete
  implementations
- Explicit handling of unsupported variants
- Pattern trade-offs and abstraction cost

File:

`lld-factory-strategy-patterns.md`

The design uses an Expense Tracker reporting example to connect object-level
patterns with backend service boundaries.

---

## Day 63 — LLD: Observer and Adapter Patterns

Day 63 extends the LLD phase with event fan-out and external integration
patterns.

Topics include:

- Observer as a one-to-many event subscription boundary
- Adapter for incompatible provider interfaces
- Combining Observer and Adapter in notification workflows
- Subscriber failure and lifecycle considerations
- Asynchronous delivery, retries, idempotency, and provider isolation
- Trade-offs of additional in-process abstraction

File:

`lld-observer-adapter-patterns.md`

The design uses a notification workflow to show how event subscribers and
provider-specific integrations can evolve independently.

---

## Day 64 — HLD Requirements and Capacity Estimates

Day 64 moves from LLD patterns into high-level system design.

Topics include:

- Functional requirements
- Non-functional requirements
- Explicit traffic assumptions
- Average versus peak request rate
- Storage estimation
- Read-heavy workload identification
- Initial architecture and scaling constraints
- Reliability and failure considerations
- Capacity assumptions versus measured production data

File:

`hld-requirements-capacity-estimates.md`

The URL Shortener is used as the example system. Capacity numbers are explicitly
illustrative assumptions rather than production measurements.

---

## Day 65 — HLD: URL Shortener Deep Dive

Day 65 deepens the Day 64 URL Shortener HLD with scaling, caching, consistency,
API evolution, reliability, and observability.

Topics include:

- Redirect and create-path deep dives
- Read-heavy workload analysis
- Cache stampede and invalidation considerations
- Read replicas and replica lag
- Partitioning versus premature sharding
- API versioning and compatibility
- Consistency requirements by operation
- Failure modes and observability
- Evidence-driven architecture evolution

File:

`url-shortener-deep-dive.md`

The deep dive extends the Day 64 HLD rather than replacing it.

---

## Day 66 — HLD: Rate Limiter

Day 66 applies the HLD process to a shared Rate Limiter.

Topics include:

- Functional and non-functional requirements
- Token-bucket rate limiting
- Shared Redis state and atomic updates
- Policy modeling and deterministic rate-limit keys
- Failure behavior and retry storms
- Hot keys and clock consistency
- Capacity planning and key cardinality
- Observability and operational trade-offs
- Regional versus globally coordinated limits

File:

`rate-limiter-hld.md`

The design uses a token bucket as the recommended starting point while keeping
algorithm, consistency, and deployment choices explicit trade-offs.

---

## Day 67 — HLD: Notification System

Day 67 applies the HLD process to a multi-channel Notification System.

Topics include:

- Notification API and asynchronous delivery
- Transactional outbox
- Durable message-broker flow
- Per-channel worker isolation
- At-least-once processing and idempotency
- Retries, backpressure, and dead-letter handling
- Ordering and scaling trade-offs
- Delivery observability and failure modes

File:

`notification-system-hld.md`

The design extends the earlier Notification Service LLD into a distributed
architecture without replacing the existing LLD artifact.

---

## Day 68 — HLD: Chat Application

Day 68 applies the HLD process to a real-time Chat Application.

Topics include:

- HTTP and WebSocket responsibilities
- WebSocket gateway architecture
- Durable message persistence
- Cross-instance fan-out
- Per-room ordering
- At-least-once delivery and idempotency
- Reconnect and offline-message recovery
- Backpressure and slow-consumer handling
- Capacity estimation
- Security and observability

File:

`chat-application-hld.md`

The design keeps live connection state at the gateway while durable messages,
membership, and read cursors remain in shared storage.

---

## Day 69 — HLD: News Feed

Day 69 applies the HLD process to a read-heavy personalized News Feed.

Topics include:

- Functional and non-functional requirements
- Fan-out-on-read versus fan-out-on-write
- Hybrid feed generation for high-fan-out authors
- Cursor pagination
- Bounded caching and stampede protection
- Asynchronous feed materialization
- Eventual consistency and freshness targets
- Capacity and scaling metrics
- Failure handling, security, and observability

File:

`news-feed-hld.md`

The design emphasizes controlling fan-out cost so both read and write paths
remain predictable as the system scales.

---

## Day 70 — HLD Review and Portfolio Consolidation

Day 70 consolidates the System Design & LLD phase with a timed review of bottlenecks, trade-offs, and CAP.

Topics reviewed:

- Capacity assumptions and bottleneck identification
- Read/write amplification, cache behavior, and queue saturation
- Consistency and availability choices during network partitions
- Reliability, observability, and graceful degradation
- Timed review of the URL Shortener, Rate Limiter, Notification System, Chat Application, and News Feed

Review artifact: `day-70-review.md`.

The portfolio index is maintained in `../projects/system-design-portfolio/README.md`.

---

## Day 71 — System Design Interview Framework

Day 71 introduces a repeatable interview flow: clarify requirements, estimate
capacity, define APIs and data models, sketch the high-level architecture,
analyze bottlenecks and failures, and defend trade-offs.

Review artifact: `interview_framework.md`.

---

## Day 72 — URL Shortener Mock Interview

Day 72 applies the interview framework to a URL Shortener in a timed mock
interview. Practice requirements, API contracts, storage, redirect latency,
cache behavior, abuse prevention, analytics, and failure handling.

Review artifact: `url-shortener-mock-interview.md`.
