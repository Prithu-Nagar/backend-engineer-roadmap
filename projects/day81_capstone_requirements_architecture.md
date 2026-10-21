# Day 81 — Capstone Requirements and Architecture

Use this document to define the scope of the capstone before implementation. Keep every statement aligned with code that exists or is explicitly planned.

## 1. Problem and users

- **Problem statement:**
- **Primary users:**
- **Main user journey:**
- **Success criteria:**
- **Explicit non-goals:**

## 2. Functional requirements

| ID | Requirement | Priority | Acceptance check |
|---|---|---|---|
| FR-1 | Create a valid resource | Must | Valid request persists and returns the documented response |
| FR-2 | Retrieve a resource or paginated list | Must | Ownership and pagination rules are enforced |
| FR-3 | Update permitted fields | Must | Invalid transitions return a predictable error |
| FR-4 | Handle missing and invalid input | Must | Error schema and HTTP status are consistent |

Replace generic requirements with the selected capstone domain before implementation.

## 3. Non-functional requirements

Record measurable targets for latency, availability, data integrity, security, maintainability, and observability. Mark each target as measured, tested, or aspirational; do not present unmeasured targets as achieved results.

## 4. Architecture

Document the request path: client → API/router → authentication and validation → service layer → repository/database → response serializer. Add background workers, cache, or external AI services only when the selected project actually needs them.

## 5. Data and API contracts

- Entities, identifiers, relationships, constraints, and indexes:
- Endpoint, method, authentication, request schema, response schema, and status codes:
- Pagination, filtering, ordering, and versioning strategy:
- Transaction boundaries and idempotency requirements:

## 6. Risks and trade-offs

| Risk | Likelihood / impact | Mitigation | Remaining limitation |
|---|---|---|---|
| Unauthorized cross-user access |  | Ownership checks and tests | |
| Invalid or duplicate requests |  | Validation and idempotency where needed | |
| Database bottleneck |  | Measure query plans before tuning | |
| Dependency outage |  | Timeouts, bounded retries, clear failure response | |

## 7. Day 81 definition of done

- [ ] Requirements and acceptance criteria are specific to the selected project.
- [ ] Architecture and request flow match intended implementation boundaries.
- [ ] API and data contracts are documented.
- [ ] Security, error behavior, and operational risks are listed.
- [ ] Open decisions are separated from implemented capabilities.

---

# Day 82 — Database and API Contracts

This section extends the Day 81 capstone plan. Replace every illustrative
field and endpoint with the selected project's actual schema and behavior.
Distinguish implemented behavior from planned work.

## 8. Data model and integrity review

| Entity | Primary key | Relationships | Constraints / indexes |
|---|---|---|---|
| User | `user_id` | Owns domain resources | Unique normalized email if applicable |
| Resource | `resource_id` | Belongs to a user | Foreign key, required fields, timestamps |
| IdempotencyRecord | `(client_id, key)` | Tracks a write request | Unique key and retention policy |

Confirm actual entities, deletion behavior, nullability, uniqueness, foreign
keys, and transaction boundaries. Add indexes only for demonstrated query
patterns and validate them against representative execution plans.

## 9. API contract review

| Method / path | Auth | Request | Success | Failure cases |
|---|---|---|---|---|
| `POST /api/v1/resources` | Required | Validated create payload | `201 Created` | `400`, `401`, `409`, `422` as defined |
| `GET /api/v1/resources/{id}` | Required | Path ID | `200 OK` | `401`, `403` or `404`, `422` |
| `GET /api/v1/resources` | Required | Bounded pagination/filter parameters | `200 OK` with items and page metadata | `400`, `401` |
| `PATCH /api/v1/resources/{id}` | Required | Allowed fields only | `200 OK` | `400`, `401`, `403` or `404`, `409`, `422` |

Define the error response schema, request ID, validation rules, pagination
defaults and maxima, and versioning policy. Choose a consistent policy for
distinguishing forbidden from not-found resources.

## 10. Transaction and security rules

- Keep multi-row state changes in one transaction when atomicity is required.
- Enforce uniqueness and referential integrity in the database, not only in code.
- Use conditional writes or locking for concurrent state transitions.
- Define idempotency behavior for retried write operations.
- Decide what happens when a database write succeeds but its response is lost.
- Authenticate protected requests and enforce ownership/role checks at the service boundary.
- Allowlist writable fields; avoid leaking secrets, stack traces, or sensitive resource existence.
- Apply bounded pagination, request-size limits, and rate limiting where appropriate.

## 11. Day 82 definition of done

- [ ] Schema, constraints, relationships, and indexes reflect the selected domain.
- [ ] API methods, paths, payloads, responses, and errors are explicit.
- [ ] Transaction boundaries and concurrent-write behavior are documented.
- [ ] Authentication, ownership, and validation rules are testable.
- [ ] Contract tests cover success, malformed input, unauthorized access, and conflicts.
- [ ] API examples match actual serializers and implementation.
- [ ] Unimplemented features and unmeasured performance targets are labeled honestly.

