# Day 87 — Capstone Tests and Observability

## Sprint objective

Add confidence in the capstone through meaningful tests and operational signals. Preserve existing application code; extend it incrementally rather than replacing working modules with assessment-only examples.

## Test plan

- [ ] Unit-test service logic, validation, and error mapping.
- [ ] Test API success responses and expected client errors.
- [ ] Verify authentication and resource ownership for both allowed and denied requests.
- [ ] Test missing, malformed, and boundary-value inputs.
- [ ] Test database constraints and transaction rollback behavior where integration infrastructure is available.
- [ ] Mock external dependencies for deterministic failure-path tests.
- [ ] Add integration tests for persistence and API-to-service-to-repository behavior.
- [ ] Ensure tests do not depend on execution order or shared mutable state.
- [ ] Run the full suite and record failures honestly.

## Observability checklist

- [ ] Emit structured logs with timestamp, severity, route/operation, and request ID.
- [ ] Redact credentials, tokens, and sensitive payload fields.
- [ ] Track request count, error rate, and latency percentiles.
- [ ] Track database pool saturation, query latency, and dependency failures.
- [ ] Define health/readiness behavior separately from deep dependency diagnostics.
- [ ] Document actionable alerts and an owner/runbook for each critical signal.

## Suggested minimal instrumentation contract

Each request should be traceable using a request ID. Logs should describe the operation and outcome without exposing secrets. Metrics should use bounded-cardinality labels; do not label metrics with raw user IDs, request IDs, or arbitrary URLs.

## Acceptance criteria

- [ ] New tests cover normal behavior, boundary cases, and important failures.
- [ ] The full existing test suite is run after the changes.
- [ ] Observability output is useful and does not leak sensitive data.
- [ ] Any unimplemented integration or deployment checks are listed as gaps.
- [ ] Performance and reliability claims are supported by measurements, not assumptions.

## Sprint summary template

- Tests added:
- Test command and result:
- Signals/log fields added:
- Known gaps:
- Next action:
