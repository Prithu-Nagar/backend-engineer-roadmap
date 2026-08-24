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
