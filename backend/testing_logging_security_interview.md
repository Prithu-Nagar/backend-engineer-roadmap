# Testing, Logging, and Security — Backend Interview Questions

Use these prompts to explain how you would build, verify, and operate a dependable backend service.

## Testing

### 1. What is the difference between unit, integration, and end-to-end tests?
- **Unit tests** isolate a function or component and verify its behavior quickly.
- **Integration tests** verify boundaries such as API-to-database interactions or authentication middleware.
- **End-to-end tests** exercise a complete user-visible flow and usually cost more to run and maintain.

Use a test pyramid suited to the system rather than relying on only one test type.

### 2. What makes a good API test suite?
Cover success cases, validation failures, authentication and authorization, missing resources, conflicts, pagination, and unexpected dependency failures. Assert status codes and response contracts, and isolate test data so results are repeatable.

### 3. How should external dependencies be tested?
Use fakes or mocks for deterministic unit tests. Keep a smaller number of integration tests against realistic dependencies to verify contracts, transactions, and configuration. Do not mock so much that the test only confirms the mock's behavior.

### 4. How do you avoid flaky tests?
Control clocks and randomness, isolate shared state, avoid arbitrary sleeps, use explicit synchronization, clean up resources, and make network dependencies deterministic. Reruns can help diagnose flakiness but should not replace fixing its cause.

## Logging and Observability

### 5. What belongs in structured logs?
Use consistent fields such as timestamp, severity, service, environment, request/correlation ID, operation, duration, and outcome. Keep messages actionable and avoid passwords, access tokens, session secrets, payment data, and unnecessary personal data.

### 6. Logs vs metrics vs traces
- **Logs** capture discrete events and contextual details.
- **Metrics** summarize behavior over time and support alerts.
- **Traces** connect spans across a distributed request path.

Use correlation or trace IDs to connect signals without making high-cardinality identifiers metric labels.

### 7. How do you choose log levels?
- `DEBUG`: diagnostic detail, usually restricted in production.
- `INFO`: meaningful normal events.
- `WARNING`: unexpected but handled conditions.
- `ERROR`: a failed operation requiring attention.
- `CRITICAL`: severe impact or imminent service-level failure.

Avoid duplicate stack traces at every layer; log an exception where useful context and ownership are clear.

## Security

### 8. How do you prevent common API security failures?
Validate inputs at trust boundaries, authenticate callers, authorize every resource operation, use parameterized SQL, apply least privilege, protect secrets, rate-limit sensitive endpoints, and keep dependencies patched. Security controls should be enforced server-side.

### 9. How should secrets be handled?
Load secrets from an approved secret manager or deployment environment, limit access, rotate them, and prevent them from entering source control, logs, error responses, and build artifacts. Treat leaked credentials as an incident requiring revocation.

### 10. What is the difference between authentication and authorization?
Authentication verifies identity. Authorization checks whether that identity may perform a specific action on a particular resource. A valid token alone must not grant access to every resource.

### 11. How do you handle security errors?
Return a stable, minimal public error response without stack traces, SQL details, secrets, or internal topology. Record the necessary internal context securely and ensure error handling does not bypass authorization or leak whether sensitive resources exist.

## Scenario Questions

### 12. A production endpoint returns intermittent 500 errors. What is your approach?
1. Check error rate, latency, recent deploys, dependency health, and correlated logs/traces.
2. Identify whether failures cluster by endpoint, tenant, region, or dependency.
3. Mitigate safely, for example by rolling back or disabling a failing feature.
4. Reproduce with a regression test and repair the root cause.
5. Verify recovery and document follow-up actions.

### 13. What quality gates belong in CI?
Run formatting/lint checks, unit tests, relevant integration tests, dependency/security checks, and build validation. Make failures visible and reproducible; use pre-commit to catch common issues locally, not as a substitute for CI.

## Quick Revision

- Tests should cover contracts, failures, authorization, and edge cases.
- Structured logs need correlation context but must not leak secrets.
- Metrics reveal trends; traces explain cross-service latency.
- Enforce least privilege and resource-level authorization.
- Diagnose incidents using evidence, mitigate safely, and add regression coverage.
