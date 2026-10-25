# Day 86 — Capstone Security and Error Handling

## Sprint objective

Harden the capstone's security boundaries and make error behavior consistent. Build on the existing Task Manager security and error-handling helpers without replacing earlier work or claiming production readiness without integration tests.

## Implementation checklist

1. Review authentication and verify authorization for every task read, update, and delete.
2. Ensure database queries include the authenticated user's ownership scope.
3. Validate request schemas and allowlist writable fields; reject unexpected input.
4. Keep SQL parameterized and use database constraints for critical invariants.
5. Review CORS, trusted hosts, CSRF protections for cookie-based sessions, and security headers.
6. Load secrets from runtime configuration; fail fast when required production settings are missing.
7. Return stable, sanitized error codes and a request ID; never return stack traces or secrets.
8. Log security-relevant events with useful context while redacting tokens and sensitive values.
9. Add negative tests for cross-user access, malformed input, missing configuration, and unexpected failures.
10. Verify dependency failure behavior, rate limiting, and rollback steps for security configuration changes.

## Error contract

- `400`: invalid request or schema.
- `401`: missing or invalid authentication.
- `403`: authenticated caller lacks permission.
- `404`: resource not found, including cases where revealing existence would leak information.
- `409`: conflict with current state or a uniqueness constraint.
- `429`: request rate limit exceeded.
- `500`: unexpected server failure with a generic client message and protected server-side diagnostics.
- `503`: temporary dependency/service unavailability when the application can identify it safely.

Use the status that matches the API contract; do not expose database messages or internal exception text to clients.

## Security and correctness notes

- The database remains the source of truth.
- Check authorization on every request; frontend filtering is not an access control.
- Avoid logging credentials, bearer tokens, CSRF tokens, or sensitive request bodies.
- Use constant-time comparison for secret token comparisons when applicable.
- Apply path normalization and containment checks to file operations.
- Do not introduce custom cryptography or store passwords with a general-purpose hash.
- Run the existing test suite before and after the increment.

## Acceptance criteria

- [ ] Resource ownership is tested for allowed and denied access.
- [ ] Error responses are consistent and do not leak implementation details.
- [ ] Security settings are explicit and production configuration fails safely.
- [ ] Input validation, database integrity, and least privilege are reviewed.
- [ ] Tests pass and any remaining integration gaps are documented.
- [ ] No performance, security, or deployment claim is made without evidence.
