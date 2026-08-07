# System Design

This directory contains core system design concepts required for backend engineering and technical interviews.

The focus is on understanding how backend systems are structured, how components communicate, and how systems can scale reliably.

---

## Completed Topics

- Monolith vs Microservices
- Caching

---

## Current Topics

- Load Balancing
- Reverse Proxy

---

## Upcoming Topics

- Redis
- Kafka
- API Gateway
- Rate Limiting
- Database Scaling
- Message Queues
- Distributed Systems

---

# Topics

## Monolith vs Microservices

Covers the architectural differences between monolithic and microservice-based applications.

Topics include:

- Monolithic architecture
- Microservices architecture
- Advantages and disadvantages
- Service boundaries
- Communication between services
- Scalability considerations

**File:** `monolith_vs_microservices.md`

---

## Caching

Covers techniques for improving system performance by storing frequently accessed data in a faster storage layer.

Topics include:

- Cache hit
- Cache miss
- TTL
- Cache invalidation
- Cache eviction
- LRU
- LFU
- Cache-aside
- Read-through
- Write-through
- Write-back
- Cache stampede
- Cache penetration
- Cache avalanche

**File:** `caching.md`

---

## Load Balancing

Load balancing distributes incoming traffic across multiple backend servers.

Topics include:

- Load balancer
- Health checks
- Horizontal scaling
- Traffic distribution
- Load-balancing strategies

**File:** `load_balancer.md`

---

## Reverse Proxy

A reverse proxy sits between clients and backend servers.

It can provide:

- Request routing
- TLS termination
- Load balancing
- Security
- Request filtering

**File:** `reverse_proxy.md`

---

# Repository Files


system-design/
├── README.md
├── monolith_vs_microservices.md
├── caching.md
├── load_balancer.md
└── reverse_proxy.md

---

# Learning Progress

| Topic                     | Status      |
| ------------------------- | ----------- |
| Monolith vs Microservices | Completed   |
| Caching                   | Completed   |
| Load Balancing            | In Progress |
| Reverse Proxy             | In Progress |
| Redis                     | Upcoming    |
| Kafka                     | Upcoming    |
| API Gateway               | Upcoming    |
| Rate Limiting             | Upcoming    |

---

# Learning Strategy

For each system design topic:

1. Understand the problem being solved.
2. Understand the major components.
3. Study how the components communicate.
4. Understand scalability and reliability trade-offs.
5. Identify common failure scenarios.
6. Practice explaining the architecture clearly.

The goal is to develop the ability to reason about backend systems rather than simply memorize system design diagrams.

