# Monolith to Modular Monolith

A modular monolith keeps a single deployable application while enforcing
clear internal module boundaries.

## Starting Point

A traditional monolith may allow routes, business logic, and data access
to become tightly coupled:

```text
HTTP Request
    |
    v
Route
    |
    v
Business Logic + Database Access
    |
    v
Database
```

This is simple initially, but responsibilities can become difficult to
separate as the application grows.

## Modular Monolith

A modular monolith introduces explicit boundaries without introducing
network calls between modules:

```text
                    Application
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 Authentication       Tasks           Users
        |                |                |
        +----------------+----------------+
                         |
                    Data Access
                         |
                         v
                      Database
```

Communication between modules remains in-process.

## Boundary Principles

Each module should have:

- A clear responsibility
- Explicit public interfaces
- Limited knowledge of other modules
- Controlled access to shared infrastructure
- Tests that can exercise the module independently

Avoid letting every module reach directly into another module's internal
implementation.

## Evolution

```text
Simple Monolith
      |
      v
Clear Module Boundaries
      |
      v
Modular Monolith
      |
      v
Extract a Service Only When Needed
```

The goal is to establish good boundaries before adding distributed-system
complexity.

## Modular Monolith vs Microservices

| Concern | Modular Monolith | Microservices |
|---|---|---|
| Deployment | Single application | Multiple services |
| Communication | In-process | Network |
| Operational complexity | Lower | Higher |
| Scaling | Application-level | Service-level |
| Data ownership | Can initially be shared | Usually service-owned |

A modular monolith is therefore an architectural middle ground rather
than simply a smaller version of microservices.
