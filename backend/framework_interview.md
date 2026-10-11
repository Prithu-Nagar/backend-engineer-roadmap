# Flask, Django, and FastAPI Interview Questions

Use these prompts to compare framework behavior and defend a choice based on
requirements, team experience, ecosystem, and operational constraints.

## Core Questions

### 1. How do Flask, Django, and FastAPI differ?

- **Flask** is a lightweight WSGI framework with a small core and a flexible
  extension ecosystem. The application team chooses many architectural pieces.
- **Django** is a batteries-included framework with an ORM, migrations, admin,
  authentication support, and established project conventions.
- **FastAPI** is an ASGI framework built around type annotations, request/response
  validation, generated OpenAPI documentation, and async endpoint support.

Choose based on the application needs and team constraints rather than a
universal ranking.

### 2. What is WSGI versus ASGI?

WSGI defines a synchronous Python web-server interface. ASGI supports
asynchronous applications and protocols such as WebSockets. Async support alone
does not make CPU-bound work faster; blocking operations can still stall an
async event loop if they are not isolated appropriately.

### 3. How is request validation handled?

Flask commonly uses explicit validation or an extension/schema library. Django
uses forms, model validation, and serializer layers such as Django REST
Framework. FastAPI uses type annotations and Pydantic models for request and
response validation. In every framework, validate untrusted input at the
boundary and enforce business rules in the appropriate service/domain layer.

### 4. How should business logic be organized?

Keep route/view handlers thin: parse and validate input, invoke application
services, and translate results into HTTP responses. Keep domain rules out of
framework-specific request objects where practical. Use repository or service
boundaries when they improve clarity, testability, or change isolation; avoid
abstraction solely for its own sake.

### 5. How do you test endpoints?

Use each framework's test client to exercise routing, serialization, status
codes, and middleware. Inject or override dependencies to isolate databases and
external APIs. Add unit tests for domain behavior and integration tests for the
important persistence and authentication boundaries. Ensure tests clean up
state and do not depend on execution order.

### 6. How do authentication and authorization differ across frameworks?

Authentication establishes the caller's identity; authorization decides what
that identity may do. Django provides an integrated user and permission system;
Flask and FastAPI typically compose authentication mechanisms and extensions or
application-defined dependencies. Regardless of framework, enforce object-level
ownership and permissions on every protected operation.

### 7. What should a production API do with errors?

Return stable status codes and a documented error schema, avoid exposing stack
traces or secrets, log diagnostic context safely, and attach a request/correlation
ID when available. Distinguish expected client errors from unexpected server
failures. Do not catch every exception and silently return success or a generic
200 response.

### 8. When would you choose async endpoints?

Async endpoints are useful when the request spends significant time awaiting
compatible I/O and concurrency is beneficial. Use synchronous handlers or
worker/process strategies when appropriate for blocking libraries or CPU-bound
work. Bound concurrency, apply timeouts, and understand how the server executes
the selected endpoint type.

### 9. What are common deployment considerations?

- Run behind a production-capable application server and configure worker counts
  for the workload.
- Keep secrets and environment-specific settings outside source control.
- Configure trusted proxy handling, TLS termination, request-size limits, and
  timeouts deliberately.
- Use health checks, structured logs, metrics, and graceful shutdown.
- Apply database migrations as a controlled release step and verify rollback
  expectations.

### 10. How do you choose among the three for a new service?

Clarify API complexity, admin and ORM needs, async/WebSocket requirements,
validation/documentation needs, team familiarity, extension ecosystem, and
operational constraints. Build a small representative vertical slice and test
maintainability and measured performance before making broad claims.

## Scenario Exercise

Design a task API with create/list/update endpoints, ownership checks, database
persistence, and integration tests. Explain how the route layer, validation,
service logic, and persistence layer would be structured in Flask, Django/DRF,
or FastAPI. Identify which framework-specific behavior you would test directly.

## Common Mistakes

- Equating `async def` with automatic performance improvements.
- Treating request validation as a replacement for authorization or business rules.
- Embedding all business logic in views or route functions.
- Assuming framework defaults remove the need for secure configuration.
- Comparing performance without the same workload, server setup, and metrics.
