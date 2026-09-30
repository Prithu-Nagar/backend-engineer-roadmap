# LLD — SOLID, Composition, and Interfaces

## Goal

Design backend components so that responsibilities are explicit, dependencies
are replaceable, and the system can evolve without forcing unrelated modules to
change together.

## Core Principles

### Single Responsibility Principle

A class should have one cohesive reason to change. In a backend service, keep
request parsing, business rules, persistence, and external notification concerns
separate.

### Open / Closed Principle

Core behavior should be extendable through abstractions instead of requiring
large conditional branches for every new implementation.

### Liskov Substitution Principle

An implementation of an interface must preserve the contract expected by its
callers. A repository adapter that changes error semantics or returns invalid
data is not a safe substitute merely because it has the same method names.

### Interface Segregation Principle

Prefer small role-specific interfaces over one large service interface. A read
use case should not depend on write, reporting, and administration operations it
does not need.

### Dependency Inversion Principle

High-level application policy should depend on abstractions. Infrastructure
adapters such as PostgreSQL, Redis, HTTP clients, and message brokers should
implement those abstractions.

## Composition over Inheritance

Prefer assembling a service from focused collaborators:

```text
Controller
    |
    v
Application Service
    |
    +----> Repository Interface ----> PostgreSQL Adapter
    |
    +----> Notification Interface -> Email Adapter
    |
    +----> Clock Interface ---------> System Clock
```

Composition makes dependencies visible at construction time and allows a test
to inject deterministic fakes without changing application logic.

## LLD Boundary Model

```text
Presentation
    |
    v
Application / Use Cases
    |
    v
Domain Rules
    |
    +----> Repository Interfaces
    +----> External-Service Interfaces
             |
             v
       Infrastructure
```

The dependency direction should point toward stable business rules. Concrete
infrastructure stays at the edge.

## Scalable Service Implications

- Keep controllers thin and free of persistence logic.
- Put business invariants in application/domain components rather than routes.
- Define transaction boundaries explicitly around use cases.
- Keep repository interfaces narrow so storage can evolve independently.
- Make external calls observable and bounded with timeouts and clear errors.
- Use composition to swap local, relational, cached, or remote implementations.
- Keep authorization checks at the application boundary and resource boundary.
- Avoid a shared mutable singleton that becomes an implicit dependency.

## Example: Task Update

```text
HTTP PUT /tasks/{id}
        |
        v
TaskController
        |
        v
UpdateTaskUseCase
        |
        +--> TaskRepository.get()
        +--> Validate ownership/status transition
        +--> TaskRepository.save()
        +--> EventPublisher.publish()
        |
        v
HTTP response
```

The controller translates transport concerns. The use case owns the business
operation. Repository and event-publishing contracts isolate infrastructure.

## Trade-offs

LLD abstractions have a cost: more interfaces, constructors, and files can make
a small application feel heavier. Use them where change, testing, multiple
adapters, or clear ownership boundaries justify the additional structure.

## Review Checklist

- Is each class cohesive?
- Can a dependency be replaced without editing business logic?
- Are interfaces small enough for their consumers?
- Does each implementation honor the interface contract?
- Are composition and dependency direction explicit?
- Are persistence and external-service concerns outside core policy?
- Are transaction, authorization, and failure boundaries clear?
