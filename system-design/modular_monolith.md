# Modular Monolith

## Day 20 — Service Boundaries

A modular monolith is a single deployable application that is internally
divided into clearly defined modules.

It provides the simplicity of a monolith while encouraging strong
internal boundaries.

---

## Why Modular Monolith?

A modular monolith avoids introducing distributed-system complexity too
early.

It can provide:

- Single deployment
- In-process communication
- Clear responsibilities
- Lower operational complexity
- Easier testing
- A path toward future service extraction

---

## Task Manager Modules

The Task Manager can be divided into logical modules:

```text
Task Manager
│
├── Authentication
├── Authorization
├── Tasks
├── Validation
├── Pagination
└── Error Handling
```

Each module should have a clear responsibility.

---

## Service Boundaries

A useful boundary should have:

- A clear responsibility
- A defined interface
- Limited knowledge of unrelated modules
- Controlled data access
- Explicit inputs and outputs

For example:

```text
Route
  ↓
Task Service
  ↓
Task Repository
  ↓
Database
```

The route should not contain all business logic.

---

## Modular Monolith vs Microservices

| Concern | Modular Monolith | Microservices |
|---|---|---|
| Deployment | Single application | Multiple services |
| Communication | Mostly in-process | Network calls |
| Operational complexity | Lower | Higher |
| Scaling | Application-level | Service-level |
| Data ownership | Can initially be shared | Usually service-owned |
| Development overhead | Lower | Higher |

---

## Architecture Evolution

The Task Manager should evolve incrementally:

```text
Simple Flask Application
        ↓
Blueprint-based Application
        ↓
Modular Monolith
        ↓
Service Layer
        ↓
Repository / Data Layer
        ↓
Potential Service Extraction
```

The goal is not to introduce microservices prematurely.

The goal is to establish boundaries that make future architectural
changes easier.

---

## Key Principle

> Establish responsibility boundaries before deployment boundaries.

A well-structured modular monolith can later be split into services when
there is a real scalability, ownership, or operational reason to do so.
