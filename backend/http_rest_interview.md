# HTTP and REST Interview Questions

## Core Questions

### 1. What happens when a client sends an HTTP request?

The client resolves the host, establishes a transport connection (typically TCP
with TLS for HTTPS), sends a request line and headers plus an optional body.
The server routes the request, applies authentication and validation, executes
the operation, and returns a status line, headers, and an optional body.
Proxies, gateways, and caches may participate in the path.

### 2. Explain common HTTP methods.

- `GET`: retrieve a representation; safe and idempotent by contract.
- `POST`: submit data or request processing; not inherently idempotent.
- `PUT`: create or replace a resource at a known URI; idempotent by contract.
- `PATCH`: apply a partial modification; idempotency depends on the patch.
- `DELETE`: remove a resource; idempotent in intended effect.
- `HEAD`: retrieve headers without the response body.

Idempotency means repeating the same request has the same intended effect, not
necessarily an identical response.

### 3. How do you choose status codes?

- `200 OK`: successful request with a response representation.
- `201 Created`: resource created; include `Location` when useful.
- `202 Accepted`: processing accepted but not completed.
- `204 No Content`: success with no response body.
- `400 Bad Request`: malformed or invalid request.
- `401 Unauthorized`: missing or invalid authentication credentials.
- `403 Forbidden`: authenticated or identified caller lacks permission.
- `404 Not Found`: resource is absent or intentionally concealed.
- `409 Conflict`: conflict with current resource state.
- `422 Unprocessable Content`: syntactically valid content fails semantic rules.
- `429 Too Many Requests`: rate limit exceeded.
- `500` / `503`: server failure / temporary unavailability.

### 4. What makes an API RESTful?

Use resource-oriented URIs, standard HTTP semantics, stateless requests,
representations, and a uniform interface. In practice, explain which REST
constraints are implemented rather than claiming an API is RESTful merely
because it returns JSON.

### 5. How should errors be represented?

Return a consistent error schema with a stable machine-readable code, a safe
human-readable message, and optional field-level details or a request ID. Avoid
leaking stack traces, secrets, SQL, or internal topology. Keep status codes
meaningful and document expected errors.

### 6. How do authentication and authorization differ?

Authentication establishes identity; authorization decides whether that
identity may perform an action on a resource. Enforce authorization server-side
for every protected operation, including object-level ownership checks.

### 7. How do you evolve an API without breaking clients?

Prefer additive changes, preserve existing field semantics, version breaking
contracts deliberately, publish deprecation timelines, and monitor usage.
Test compatibility with representative old clients before removing behavior.

### 8. How would you protect a write endpoint against retries?

For operations that must not be duplicated, accept an idempotency key, scope it
to the caller and operation, persist the key with the outcome, and define
expiration and concurrent-request behavior. A key alone is not enough without
atomic persistence and replay semantics.

## Quick Practice

For each answer, explain one trade-off and give a concrete example from the Task
Manager API. Keep answers concise, then follow up with a failure mode or test.
