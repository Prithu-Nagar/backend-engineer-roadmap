# Day 86 — Security and Failure Modes

## Objective

Review security as a system property: minimize privileges, isolate tenants, validate trust boundaries, and design explicit behavior for dependency and abuse scenarios.

## Threat-model checklist

1. **Assets:** user data, credentials, tokens, service secrets, and audit records.
2. **Trust boundaries:** client-to-edge, API-to-service, service-to-database, and service-to-model/tool.
3. **Threats:** broken object-level authorization, injection, credential theft, replay, request flooding, data leakage, and dependency compromise.
4. **Controls:** authentication, per-resource authorization, parameterized queries, schema validation, least privilege, secret rotation, rate limits, and audit events.
5. **Verification:** negative tests, dependency scanning, access review, and incident drills.

## Failure-mode table

| Failure mode | Expected behavior | Evidence to monitor |
|---|---|---|
| Authentication provider unavailable | Fail closed for protected operations; return a bounded error | Auth dependency errors and latency |
| Database unavailable | Return a sanitized service error; do not leak internals | Error rate, pool saturation, query latency |
| Rate limit exceeded | Return `429` with a documented retry policy where appropriate | Rejection count by route/client |
| Invalid or expired token | Reject the request; never silently downgrade privileges | Authentication failure counts |
| Cross-tenant resource ID | Deny access without revealing another tenant's data | Authorization denials and audit events |
| Secret accidentally exposed | Rotate/revoke it, assess scope, and preserve incident evidence | Secret-scanner alerts and access logs |

## Design principles

- Authenticate the caller, then authorize every resource operation.
- Apply tenant/user scope inside data-access predicates, not only in UI logic.
- Keep secrets outside source control and avoid logging tokens or personal data.
- Use bounded timeouts, retries only where safe, and explicit dependency failure behavior.
- Return stable error codes and request IDs; keep stack traces in protected server logs.
- Use TLS, secure cookie settings, CSRF defenses where cookie authentication is used, and restrictive CORS/host policies.
- Treat security headers and rate limits as layers, not substitutes for authorization.

## Review questions

- Which controls prevent a valid user from reading another user's object?
- What happens if an authentication dependency times out?
- How are leaked credentials revoked and rotated?
- Which actions require immutable audit events?
- What is the rollback plan if a security configuration blocks legitimate traffic?

## Acceptance criteria

- [ ] Threats and trust boundaries are documented.
- [ ] Each critical failure has an explicit response and observable signal.
- [ ] Negative authorization and validation tests are included.
- [ ] Client errors are sanitized while server diagnostics remain access-controlled.
