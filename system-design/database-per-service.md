# Database-per-Service

Database-per-service is a microservice architecture pattern where each
service owns its database or schema boundary.

The service that owns the data is responsible for its schema, migrations,
consistency rules, and access patterns.

---

## Core Principle

```text
                +----------------+
                |   API Gateway  |
                +--------+-------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
   +-------------+ +-------------+ +-------------+
   | User Service| | Task Service| | URL Service |
   +------+------+ +------+------+ +------+------+
          |               |               |
          v               v               v
     User DB          Task DB         URL DB
```

A service should normally access its own database rather than directly
querying another service's database.

---

## Why Use It?

Database ownership reinforces service boundaries.

Benefits include:

- Independent schema evolution
- Clear ownership of data
- Independent scaling
- Reduced coupling
- Independent deployment of data changes
- Better alignment between domain and persistence boundaries

---

## Service Ownership

Consider a system with separate services:

```text
User Service
    |
    +--> user_db

Order Service
    |
    +--> order_db

Notification Service
    |
    +--> notification_db
```

The Order Service should not directly execute SQL against `user_db`.

If Order Service needs user information, it can communicate through an API
or an asynchronous event.

---

## Cross-Service Communication

A common pattern is:

```text
Service A
   |
   | HTTP / RPC / Event
   v
Service B
   |
   v
Service B Database
```

This keeps database ownership inside the service boundary.

---

## Data Duplication

Distributed systems sometimes duplicate a small amount of data to avoid
synchronous cross-service calls.

For example:

```text
User Service
     |
     | UserUpdated event
     v
Order Service
     |
     v
Local user summary
```

The duplicated data may be eventually consistent.

The design should distinguish:

- Source of truth
- Read model / local projection
- Synchronization mechanism
- Consistency requirements

---

## Transactions

A local database transaction is straightforward:

```text
BEGIN
  |
  +--> Update Service A data
  |
COMMIT
```

A transaction spanning multiple service-owned databases is significantly more
complex.

Instead of assuming distributed ACID transactions are always required,
consider:

- Idempotent operations
- Events
- Outbox pattern
- Saga-style workflows
- Compensating actions

The correct choice depends on the business consistency requirements.

---

## Trade-offs

| Aspect | Shared Database | Database-per-Service |
|---|---|---|
| Data access | Easy across domains | Restricted by ownership |
| Schema coupling | Higher | Lower |
| Independent scaling | Limited | Stronger |
| Cross-domain queries | Easier | More complex |
| Transactions | Simpler | More difficult |
| Service autonomy | Lower | Higher |
| Operational overhead | Lower | Higher |

Database-per-service is not automatically better. It becomes valuable when
independent service ownership and deployment justify the additional
distributed-system complexity.

---

## Interview Checklist

- What does database ownership mean?
- Why should services avoid direct access to another service's database?
- How are cross-service data requirements handled?
- What is eventual consistency?
- Why can distributed transactions become difficult?
- When would a shared database still be reasonable?
- How do events and local projections reduce cross-service coupling?
