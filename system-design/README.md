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

| Topic | Status |
|---|---|
| Monolith vs Microservices | Completed |
| Reverse Proxy | Completed |
| Load Balancing | Completed |
| Caching | Completed |
| Database Scaling | Completed |
| Redis | Completed |
| Authentication & Authorization | Completed |

---

## Upcoming Topics

- Kafka
- API Gateway
- Rate Limiting
- Distributed Systems
- Message Queues
- Event-Driven Architecture
