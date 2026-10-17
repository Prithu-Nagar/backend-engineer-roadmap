# Day 78 — End-to-End Backend Coding Exercise

## Objective

Complete a timed, end-to-end Task Manager API exercise that connects request
validation, business rules, persistence, SQL, tests, and API behavior. Treat
this as an interview simulation rather than a replacement for the existing
project implementation.

**Suggested time:** 60–75 minutes.

## Requirements

- Create a task with a non-empty title of at most 200 characters.
- Retrieve one task by ID.
- List tasks with validated, bounded pagination.
- Update a task title and/or status.
- Delete a task and return a consistent response.
- Use stable error responses for validation errors and missing resources.
- Keep storage access behind a repository/service boundary.
- Preserve existing authentication and ownership rules when integrating with
  the full Task Manager project.

## Suggested API Contract

| Method | Endpoint | Success |
| --- | --- | --- |
| `POST` | `/api/v1/tasks` | `201 Created` |
| `GET` | `/api/v1/tasks/{task_id}` | `200 OK` |
| `GET` | `/api/v1/tasks?limit=20&offset=0` | `200 OK` |
| `PATCH` | `/api/v1/tasks/{task_id}` | `200 OK` |
| `DELETE` | `/api/v1/tasks/{task_id}` | `204 No Content` |

Use `400` for malformed or invalid input and `404` for a task that does not
exist. Do not return stack traces or sensitive implementation details.

## Implementation Sequence

1. Define the request/response contract and allowed task statuses.
2. Implement service-level validation and business rules.
3. Use a repository interface so the service is testable without a database.
4. Implement the endpoints and consistent error envelope.
5. Add unit tests for validation and service behavior.
6. Add API tests for success, invalid input, missing IDs, and pagination.
7. Run the repository's configured tests and lint checks.
8. Review SQL constraints and indexes against the actual query patterns.

## Minimum Test Matrix

- Empty, whitespace-only, and overlong titles are rejected.
- Valid creation returns the expected status and resource identifier.
- Missing task IDs return `404`.
- Unsupported statuses are rejected.
- Pagination rejects negative offsets and out-of-range limits.
- Updates do not silently ignore an invalid field.
- Deleting a missing task has documented behavior.
- Existing authorization and ownership tests still pass.

## Review Checklist

- [ ] Validation is performed at the API boundary and service boundary where
      appropriate.
- [ ] Business logic is not duplicated across route handlers.
- [ ] Database writes preserve constraints and transaction boundaries.
- [ ] Error responses are stable and safe.
- [ ] Tests cover both successful flows and failure paths.
- [ ] Existing files and project behavior were preserved.
- [ ] No performance, deployment, or scale claims are made without evidence.
