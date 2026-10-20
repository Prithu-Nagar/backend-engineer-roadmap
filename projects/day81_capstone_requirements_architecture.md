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
