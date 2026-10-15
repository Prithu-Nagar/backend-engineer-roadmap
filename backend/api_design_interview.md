# API Design — Backend Interview Questions

Use these prompts to explain resource modeling, stable contracts, validation, error handling, and backward-compatible API evolution.

## Resource and Contract Design

### 1. What makes a REST API well designed?
Use resource-oriented URLs, appropriate HTTP methods and status codes, consistent representations, explicit validation, predictable errors, and documented behavior. Keep the contract independent of internal database table names where possible.

### 2. How do you choose HTTP methods?
- `GET` retrieves a representation and should not change server state.
- `POST` commonly creates a resource or initiates an operation.
- `PUT` replaces a resource representation and is generally idempotent.
- `PATCH` applies a partial update; define the patch semantics explicitly.
- `DELETE` removes a resource or marks it deleted, with behavior documented.

Idempotency depends on the endpoint's defined semantics, not only the method name.

### 3. How should an API validate requests?
Validate types, required fields, ranges, formats, and cross-field rules at the boundary. Return actionable field-level errors without exposing stack traces or internal implementation details. Enforce authorization and business invariants separately from basic schema validation.

### 4. How do you design consistent errors?
Use a stable error envelope with a machine-readable code, safe human-readable message, optional field details, and a request or correlation ID. Map expected domain errors to suitable status codes and log unexpected failures with protected diagnostic context.

### 5. How do you handle pagination?
Choose offset pagination for simpler datasets and page-number navigation, or cursor/keyset pagination for large or frequently changing datasets. Define stable ordering, page-size limits, cursor validation, and whether newly inserted records can appear during traversal.

## Reliability and Compatibility

### 6. What is an idempotency key?
A client-provided key lets a server recognize retries of the same logical operation, such as a payment or order creation. Persist the key with request identity and outcome, define expiration and conflict behavior, and prevent two concurrent requests with the same key from executing the operation twice.

### 7. How do you evolve an API without breaking clients?
Prefer additive optional fields, preserve existing meanings, document deprecation windows, and monitor usage before removal. Version only when compatibility requirements justify it; test old and new clients against the contract.

### 8. Where should authentication and authorization occur?
Authenticate the caller, then authorize each operation against the requested resource and action. Do not rely on hidden UI controls or a valid token alone. Apply least privilege and avoid leaking whether protected resources exist when that distinction is sensitive.

### 9. What should API observability include?
Measure request count, error rate, latency percentiles, saturation, and dependency timings. Log route templates rather than raw identifiers as metric labels, and never log credentials or sensitive request bodies.

## Design Exercise

Design `POST /v1/tasks` and `GET /v1/tasks` for a multi-user task manager. Explain:

- Request and response schemas, status codes, and validation errors.
- Authentication and ownership checks.
- Pagination and deterministic sorting.
- Duplicate submission and retry behavior.
- Database constraints, tests, and API documentation.
- How the contract could evolve without breaking existing clients.
