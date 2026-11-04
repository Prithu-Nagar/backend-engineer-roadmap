# Task Manager REST API

The Task Manager is the primary backend project for the Backend Engineer Roadmap.

The project is being developed incrementally alongside the roadmap so that concepts learned each day are applied to a realistic backend application.

---

## Project Goals

The Task Manager API is designed to demonstrate:

- REST API development
- Flask application structure
- CRUD operations
- Request and response handling
- Error handling
- Authentication
- JWT authentication
- Authorization
- Role-Based Access Control (RBAC)
- Database integration
- API security
- Production-oriented backend design

---

# Current Architecture

The project is being developed incrementally.

The integrated Flask application now enforces the authentication flow:

```text
Client → Register / Login → Password verification → Signed JWT
  → Bearer token validation → Database user lookup
  → Ownership / role check → Task resource
```

Authentication determines who the user is.

Authorization determines what the authenticated user is allowed to do.

Features
Task Management

The project demonstrates authorization rules for:

- Create task
- Read task
- Update task
- Delete task

Update/delete behavior is represented in the service and test learning artifacts.
The Phase 2 Day 3 database foundation is persistent and migration-backed.
Phase 2 Day 4 integrates registration, login, JWT validation, authenticated
task creation/listing/detail retrieval, and task ownership into the Flask app.
Full update/delete CRUD, expanded validation, and pagination acceptance remain
separate project milestones.

Authentication verifies the identity of the user.

The integrated API now provides:

- `POST /api/auth/register` — create a regular user account
- `POST /api/auth/login` — verify credentials and issue a JWT
- `GET /api/auth/me` — return the authenticated user's profile
- `Authorization: Bearer <token>` — authenticate protected requests

Passwords are stored using Werkzeug PBKDF2-SHA256 password hashing; plaintext
passwords are never stored or returned. JWTs are signed with `JWT_SECRET`,
include subject/issued-at/expiry claims, and default to a 30-minute lifetime.
The user is reloaded from the database on each authenticated request, so the
token does not independently grant access after the account is removed.

JWT tokens contain information required to identify the authenticated user.

JWT Authentication

The authentication flow is:

```text
User
  ↓
Login Request
  ↓
Verify Credentials
  ↓
Create JWT
  ↓
Return Access Token
  ↓
Client Stores Token
  ↓
Client Sends Token
  ↓
Backend Validates JWT
  ↓
Authenticated User
```

The JWT contains user-related claims such as:

User ID
Username
Role
Issued-at time
Expiration time
Authorization

Authorization is performed after authentication.

The integrated task endpoints apply ownership filtering: regular users can
create and list their own tasks and retrieve only their own task records.
Requests for another user's task return `404` to avoid revealing whether the
resource exists. Administrators can list and retrieve tasks across owners.

The project retains role-based authorization.

Example roles:

Admin
User

Permissions are associated with roles.

Example:

Admin
```text
 ├── create_task
 ├── read_task
 ├── update_task
 ├── delete_task
 └── manage_users
```

User
```text
 ├── create_task
 ├── read_task
 ├── update_task
 └── delete_task
```
Role-Based Access Control

RBAC allows permissions to be associated with roles rather than implementing separate authorization rules for every user.

The basic flow is:

Authenticated User
```text
        ↓
```
      Role
```text
        ↓
```
   Permissions
```text
        ↓
```
Permission Check
```text
        ↓
```
Allow / Deny

For example, an administrator can access user-management functionality while a normal user cannot.

Resource Authorization

Authorization can also depend on resource ownership.

For example:

```text
User A
   ↓
```
Owns Task 1
```text
   ↓
```
Can access Task 1

A normal user should not automatically be allowed to modify another user's task.

An administrator can be granted broader access.

Therefore, authorization can involve both:

Role permissions
Resource ownership
HTTP Authorization Responses

The project distinguishes between authentication and authorization failures.

401 Unauthorized

Returned when authentication is required but the user has not successfully authenticated.

403 Forbidden

Returned when the user is authenticated but does not have permission to perform the requested operation.

Example:

No valid authentication
```text
        ↓
```
       401

Authenticated
```text
      ↓
```
Permission check
```text
      ↓
```
Permission denied
```text
      ↓
```
       403
Project Structure

The project is being expanded incrementally as new backend concepts are introduced.

Relevant authentication and authorization files include:

projects/
```text
└── task-manager/
    ├── README.md
    └── jwt_authentication.py
```

Backend-level authentication and authorization implementations are maintained separately from the project-specific implementation.

Development Strategy

The Task Manager follows the same incremental approach as the roadmap.

Each major concept is first learned independently and then applied to the project.

Example progression:

Flask Basics
```text
      ↓
```
Routing
```text
      ↓
```
REST API
```text
      ↓
```
CRUD
```text
      ↓
Request / Response Handling
      ↓
```
Error Handling
```text
      ↓
```
Authentication
```text
      ↓
```
JWT
```text
      ↓
```
Authorization
```text
      ↓
```
RBAC

This keeps the project aligned with the concepts being studied.

Current Progress

Completed project concepts:

Task Manager REST API setup
Flask routing
CRUD operations
Request and response handling
Authentication and authorization architecture
JWT authentication
JWT access-token handling
Authorization
Role-Based Access Control

Historical learning progress:

The repository now includes authorization, validation, error handling,
pagination, logging, health-check, security-hardening, and automated-test
exercises. These modules are not all wired into one project-specific runtime.
See the Day 90 acceptance checklist near the end of this README before treating
the capstone as complete.

Relevant files:

- `auth.py` and `auth_routes.py` — integrated password/JWT authentication
- `flask_routing.py` — authenticated task routes and ownership filtering
- `tests/test_phase2_day4_auth.py` — authentication and ownership integration tests

---

## Testing

Day 15 introduces comprehensive testing for the Task Manager API.

Test Strategy

The test suite covers:

- Authentication and authorization flows
- Task CRUD operations
- Permission-based access control
- Error handling and validation
- Edge cases and invalid inputs

Test Structure

Tests are organized by functionality:

- `conftest.py` — Pytest configuration and shared fixtures
- `test_tasks.py` — Task operation tests (CRUD, filtering, permissions)
- `test_auth.py` — Authentication and authorization tests

Pytest Fixtures

Fixtures provide reusable test data:

- `app` — Flask test application
- `client` — Test client for simulating requests
- `runner` — CLI test runner
- `auth_headers` — Mock authentication headers
- `user_data` — Sample user data
- `admin_data` — Sample admin user data
- `task_data` — Sample task data
- `multiple_tasks` — Multiple task samples

Test Coverage

Task Tests:

- Creating tasks
- Retrieving tasks
- Updating tasks
- Deleting tasks
- Filtering and searching
- Permission checks
- Resource ownership validation

Authentication Tests:

- Login with valid credentials
- Login with invalid credentials
- Missing authentication headers
- Invalid token formats
- Expired tokens

Authorization Tests:

- User permissions for task operations
- Admin access to admin operations
- Permission denial for unauthorized users
- Role-based access control

Token Tests:

- Token generation
- Token validation
- Token refresh
- Token expiration
- Logout

---

## API Validation and Schemas

Day 16 introduces validation and schema boundaries for the Task Manager API.

The project now includes:

- Request validation
- Required field validation
- Type validation
- String validation
- Priority validation
- Allowed request fields
- Response field filtering
- Input sanitization

Relevant files:

- `validation.py`
- `schemas.py`

Validation ensures that invalid or unexpected input is rejected before application logic processes it.

Schemas define which fields are accepted for task creation, task updates, and API responses.

---

## Pagination, Filtering and Sorting

Day 17 extends the Task Manager with pagination, filtering, and sorting.

The implementation supports:

- Page-based pagination
- Configurable page size
- Completion filtering
- Sorting by allowed fields
- Ascending and descending ordering
- Pagination metadata
- Validation of pagination parameters
- Validation of sort fields and sort order

Relevant files:

- `pagination.py`
- `tests/test_pagination.py`

Pagination metadata includes:

- Current page
- Page size
- Total records
- Total pages
- Whether a next page exists
- Whether a previous page exists

The implementation keeps pagination, filtering, and sorting as separate
operations so the behavior can later be moved into database-backed queries.

---

## Standardized Errors + Generators

Day 18 extends the Task Manager with:

- Consistent API error responses
- Standard error codes
- HTTP status-code conventions
- Generator-based task processing
- Lazy evaluation
- Generator pipelines

All application errors should follow a consistent structure:

```json
{
    "error": {
        "code": "TASK_NOT_FOUND",
        "message": "The requested task was not found."
    }
}
```

Examples:

BAD_REQUEST — 400
UNAUTHORIZED — 401
FORBIDDEN — 403
TASK_NOT_FOUND — 404
CONFLICT — 409
Generator Pipeline

Task processing can be performed lazily:

Tasks
```text
  ↓
```
Task Generator
```text
  ↓
```
Completion Filter
```text
  ↓
```
Priority Filter
```text
  ↓
```
Result

The generator pipeline avoids creating unnecessary intermediate lists
and demonstrates lazy evaluation in the project.

Day 18 Files
error_handling.py
generators.py
tests/test_error_handling.py
tests/test_generators.py

---

# Production-Style Refactor

Day 20 begins the transition from the Task Manager learning project
toward a more structured backend application.

The architecture now emphasizes:

- Application factory
- Configuration separation
- Service boundaries
- Modular organization
- Database design
- Separation of responsibilities

## Target Architecture

```text
Client
  |
  v
Flask Application
  |
  +----------------------+
  |                      |
  v                      v
Authentication       Task Module
  |                      |
  v                      v
Authorization        Task Service
                         |
                         v
                    Task Repository
                         |
                         v
```

---

## Test Approach

Tests follow the Arrange-Act-Assert pattern:

1. Arrange — Set up test data and fixtures
2. Act — Execute the operation being tested
3. Assert — Verify the results

---

## Phase 2 Day 4 — Integrated Authentication

Configuration:

- `JWT_SECRET` — signing secret; use a unique secret of at least 32 characters in production
- `JWT_ACCESS_TOKEN_TTL_SECONDS` — access-token lifetime (default: `1800`)
- `PASSWORD_MIN_LENGTH` — registration password minimum (default: `8`)

Production startup validates the JWT signing secret. Do not commit secrets.
Public registration always creates the `user` role; administrative roles must
be provisioned through a trusted administrative process.

Example:

```bash
curl -X POST http://localhost:5000/api/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{"username":"alice","email":"alice@example.com","password":"correct-horse"}'

curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username":"alice","password":"correct-horse"}'

curl http://localhost:5000/api/auth/me \\
  -H "Authorization: Bearer <access-token>"
```

The existing Alembic users/tasks migration already contains the password hash,
role, and task owner columns, so this milestone requires no schema migration.

## Remaining Work

- Complete task update/delete CRUD and broader filtering/pagination acceptance.
- Add token refresh/revocation only if the later project scope requires it.
- Complete API documentation and fresh-environment acceptance.

The project will continue evolving as new backend, system-design, SQL, and Python concepts are introduced throughout the roadmap.

---

## Dockerization

Day 41 packages the Task Manager backend as a Docker image.

Dockerfile:

`projects/task-manager/Dockerfile`

Build from the repository root:

```bash
docker build -f projects/task-manager/Dockerfile -t task-manager-api .
```

Run the container:

```bash
docker run --rm -p 5000:5000 task-manager-api
```

The container listens on port `5000` and runs the existing Flask application.
The container applies Alembic migrations before starting Gunicorn. A plain
`docker run` uses the SQLite fallback, which is ephemeral with the container;
Docker Compose uses PostgreSQL with a named volume.

Docker Compose is intentionally deferred to Day 42.

---

## Docker Compose

Day 42 adds a multi-container local environment around the existing
Dockerized Task Manager.

The repository root `docker-compose.yml` runs:

- Flask application
- PostgreSQL
- Redis

The application receives dependency locations through:

- `DATABASE_URL`
- `REDIS_URL`

The database and Redis services include health checks, and PostgreSQL data is
stored in a named Docker volume.

The application code is not replaced. Docker Compose adds orchestration around
the Day 41 image. PostgreSQL starts empty and the app applies the root Alembic
migrations; the standalone Day 41/42 SQL exercises are not mounted as schema
initializers.

---

## Day 44 — CI Pipeline & Test Coverage

Day 44 extends the Task Manager project's automated quality checks with test
coverage reporting through the repository GitHub Actions workflow.

Coverage is used as a feedback signal alongside functional tests. It does not
replace meaningful test cases or review of untested behavior.

The repository workflow runs the Task Manager test suite with `pytest-cov` and
prints a missing-lines report for CI review.

---

## Day 45 — Deployment Readiness

Day 45 prepares the Task Manager for production-style serving behind a reverse
proxy and application server.

Added/updated:

- Environment-driven application configuration
- WSGI entry point at `backend/wsgi.py`
- Gunicorn as the production WSGI server
- Deployment-ready Docker startup command
- Runtime configuration documentation

Production request flow:

```text
Client
  |
  v
Reverse Proxy
  |
  v
Gunicorn
  |
  v
Flask Task Manager
  |
  +-------> Database
  |
  +-------> Redis
```

Build the image from the repository root:

```bash
docker build -f projects/task-manager/Dockerfile -t task-manager-api .
```

Production secrets should be supplied through the deployment platform's secret
management mechanism rather than committed to the repository.

---

## Day 46 — Health Checks + Structured Logging

Day 46 adds production-oriented health checks and structured logging support.

Added:

- `health_checks.py` for liveness and readiness logic
- `structured_logging.py` for JSON log formatting
- `tests/test_health_checks.py` for readiness and failure-path coverage

Health semantics:

- **Liveness** answers whether the process is alive and able to serve requests.
- **Readiness** answers whether the instance should receive traffic.
- A failed required dependency returns HTTP `503` from readiness.

The backend Flask application registers:

- `GET /health/live`
- `GET /health/ready`

Structured logs include stable operational fields such as request ID, method,
path, status code, and duration when those fields are available. Sensitive
request values should not be written to logs.

---

## Day 47 — Security Hardening

Day 47 adds a security hardening pass to the Task Manager project.

Added:

- `security_hardening.py`
- `tests/test_security_hardening.py`

The hardening layer demonstrates:

- Explicit CORS origin allow-listing
- CSRF requirements for cookie-authenticated state-changing requests
- Constant-time CSRF token comparison
- Production secret validation
- Baseline browser-facing security headers

Security-sensitive values are treated as secrets and should be supplied through
the deployment environment or secret-management system rather than committed
to source control or written to logs.

---

## Day 61 — LLD Data Structures Review

Day 61 adds a small domain-focused LLD review artifact without replacing the
existing Task Manager implementation.

Added:

- `lld_data_structures.py`

The review models:

- `TaskStatus` as an explicit domain type
- Task dependencies as a set of task IDs
- A `TaskStore` interface for persistence behavior
- An in-memory store for deterministic examples
- A `TaskService` that owns the task-completion use case

The example demonstrates composition and dependency inversion while keeping the
existing Flask application structure intact. It also makes the task dependency
invariant explicit: a task cannot be completed while one of its dependencies is
still incomplete.

---

## Day 71 — Resume Bullet Preparation

Day 71 turns the existing Task Manager implementation into evidence-based
resume bullets covering REST API development, authentication and authorization,
pagination, tests, logging, and operational practices.

Draft artifact: `resume_bullets.md`.

Use only claims supported by the repository. Add performance metrics only after
measuring them, and do not claim deployment or scale without evidence.

---

## Day 83 — Capstone Implementation Sprint 1

Added `task_service.py` as a framework-independent domain-service increment.
It validates task payloads, allowlists writable fields, generates stable
in-memory IDs, and raises explicit validation/not-found exceptions. The
implementation is intentionally an in-memory development artifact; integrate
it with the existing database-backed model/repository before wiring it into
production routes.

The sprint plan is documented in `../day83_capstone_implementation_sprint1.md`.

---

## Day 86 — Security and Error Handling

The capstone increment is documented in `../day86_capstone_security_error_handling.md`.
Review the existing `security_hardening.py` and `error_handling.py` helpers against
the plan, then add integration-level authorization and error-contract tests before
treating the controls as complete.


---

## Day 90 Capstone Acceptance Checklist

The roadmap exercises are present, but the capstone should not be described as
a complete production-style API until each item is verified in the integrated
application:

- [ ] One Task Manager application entry point wires the project routes and services.
- [ ] Create, list, retrieve, update, and delete HTTP endpoints work end to end.
- [ ] A project-specific ORM model/repository persists tasks across restarts.
- [ ] Database migrations and local database setup are documented and tested.
- [ ] Authentication and resource-ownership authorization are enforced at route level.
- [ ] Validation, standardized errors, pagination, and filtering are integrated.
- [ ] Tests cover success, invalid input, not found, unauthenticated, and forbidden cases.
- [ ] Docker and Compose start the actual Task Manager application and dependencies.
- [ ] CI runs the complete test suite from the repository root.
- [ ] Configuration, secrets, logging, health checks, and deployment steps are documented.

A passing test suite for individual learning modules is useful evidence, but it
does not replace end-to-end verification of the integrated capstone.

---

## Phase 2 — Day 1 Repository Review (1 November 2026)

Phase 2 dates in this repository are shifted one day earlier than the dates
printed in the sprint DOCX: Day 1 is 1 November 2026, Day 2 is 2 November, and
Day 3 is 3 November. The initial review mapped the existing application entry
point, route modules, configuration, task-service helpers, validation,
authentication, authorization, persistence gaps, Docker setup, and tests. The
existing helper tests provide a useful baseline, but passing module-level tests
do not establish end-to-end HTTP/database behavior.

The implementation decision is to preserve useful learning modules, avoid a
wholesale rewrite, and integrate the existing pieces behind one canonical Task
Manager application. The ORM models and initial Alembic migration now provide
durable persistence; route-level ownership enforcement and integrated API
behavior remain implementation work.

---

## Phase 2 — Day 2 (2 November 2026): MVP Scope, API Contract and Configuration

### Canonical implementation and scope

The canonical implementation for the integrated MVP is **Flask**, using the
existing repository entry point at `backend/app.py` and shared environment
configuration at `backend/config.py`. PostgreSQL is the target persistent
database. The existing project-level Python files remain useful learning
artifacts; the Phase 2 Day 3 database foundation is now integrated, but the
project-specific API is not yet a complete persistent application.

The five-day MVP is limited to:

- User registration and login with password hashing and JWT access tokens.
- Authenticated task creation, listing, retrieval, update and deletion.
- Per-user task ownership; an administrator may access all tasks.
- Task status and priority validation, list filtering and bounded pagination.
- PostgreSQL persistence, reproducible schema initialization, automated tests
  and Docker-based local setup.

Out of scope for this MVP are refresh-token rotation, password reset/email
flows, role/permission administration endpoints, Redis-backed behavior,
background jobs, a frontend, and production deployment. Existing exercises
for those topics remain separate unless a later day's task explicitly
integrates them.

### Locked API contract

All application endpoints use the `/api/v1` prefix. JSON is used for request
and response bodies. Task endpoints require
`Authorization: Bearer <access-token>`.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | Register a user | 201 |
| POST | `/api/v1/auth/login` | Verify credentials and issue an access token | 200 |
| GET | `/api/v1/tasks` | List the authenticated user's tasks | 200 |
| POST | `/api/v1/tasks` | Create a task for the authenticated user | 201 |
| GET | `/api/v1/tasks/{task_id}` | Retrieve an owned task | 200 |
| PATCH | `/api/v1/tasks/{task_id}` | Partially update an owned task | 200 |
| DELETE | `/api/v1/tasks/{task_id}` | Delete an owned task | 204 |

A regular user can access only their own tasks. An administrator can access
tasks across users. Missing/invalid authentication returns `401`; an
authenticated but disallowed operation returns `403`; missing tasks return
`404`; invalid input returns `422`; duplicate username/email returns `409`.

Registration accepts `username`, `email` and `password`. Login accepts
`email` and `password`. Passwords are never returned by the API; only a
password hash is stored.

Task creation accepts:

```json
{
  "title": "Prepare release",
  "description": "Write release notes",
  "status": "pending",
  "priority": "medium"
}
```

`title` is required (1–200 characters after trimming). `description` is
optional. `status` is one of `pending`, `in_progress`, or `completed` and
defaults to `pending`. `priority` is one of `low`, `medium`, or `high` and
defaults to `medium`. Updates accept any non-empty subset of those four task
fields. Clients cannot set `id`, `user_id`, timestamps, role, or password
fields.

The list endpoint supports `status` and `priority` filters, plus `page`
(default `1`) and `per_page` (default `20`, maximum `100`). Results are ordered
by `created_at` descending, with `id` descending as a stable tie-breaker.
Timestamps are ISO-8601 UTC values. Task responses expose `id`, `title`,
`description`, `status`, `priority`, `created_at` and `updated_at`; ownership
and authentication fields remain internal.

Errors use the existing standard envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "A human-readable explanation."
  }
}
```

### Database contract

`sql/task_manager_schema.sql` is the canonical PostgreSQL schema reference.
It defines:

- `users`: identity primary key, unique username/email, password hash,
  `user`/`admin` role and creation timestamp.
- `tasks`: identity primary key, required owner foreign key with cascade delete,
  title, optional description, status, priority and creation/update timestamps.
- Check constraints for role, non-empty title, status and priority.
- Owner/status and owner/priority indexes for the MVP's list filters.

Task completion is represented by the single `status` field; there is no
separate boolean `completed` column to drift out of sync. Seed users contain an
intentionally unusable password sentinel and cannot log in until real password
hashes are supplied. `sql/task_manager_schema.sql` remains a reference/demo
script; the versioned schema and clean-database initialization are implemented
by the Alembic migration in the root `migrations/` directory.

### Configuration and environment

The existing `backend/config.py` is the shared configuration source. The
project's `.env.example` lists the supported local variables:

| Variable | Purpose |
| --- | --- |
| `APP_ENV` | Runtime environment (`development`, `testing`, `production`) |
| `APP_DEBUG` | Enable Flask debug mode locally; keep false in production |
| `SECRET_KEY` | Secret used by Flask/JWT-related application components |
| `DATABASE_URL` | PostgreSQL connection URL |
| `REDIS_URL` | Optional Redis connection URL; not required by the MVP |

Copy `.env.example` to `.env` and export its values in the shell before
starting the application. The repository does not currently auto-load `.env`
files. Use a unique local secret; never commit `.env` or production secrets.
The current configuration has a development-only fallback secret, which must
not be used for production. Redis is documented for compatibility with the
shared configuration but is not a Day 2 runtime dependency.

### Folder and ownership boundaries

The existing repository layout is retained. The integration will use these
boundaries rather than moving or duplicating the current learning modules:

```text
backend/
  app.py                 # Flask entry point / application factory integration
  config.py              # shared environment-based configuration

projects/task-manager/
  .env.example           # local configuration template
  tests/                 # project tests
  schemas.py              # request/response field allow-lists
  authorization.py       # authorization rules
  validation.py          # reusable input validation
  ...                    # existing focused learning modules

sql/
  task_manager_schema.sql # canonical PostgreSQL schema reference
```

Day 3 adds `backend/models.py`, shared SQLAlchemy extensions, and the root
`migrations/` directory. This section records the agreed API contract; it does
not claim that the endpoints or complete persistent application are already
implemented.

### Contract walkthrough (planned demo)

1. Initialize a clean PostgreSQL database with `flask db upgrade`.
2. Register a user, then log in to obtain a bearer token.
3. Create a task and retrieve it using the returned task ID.
4. List tasks with a status filter and page size.
5. Attempt to access another user's task and verify the ownership denial.
6. Update the task status, then delete it.

The walkthrough becomes executable when the API integration is completed; it
is a contract/demo path, not a claim that these routes are runnable today.



---

## Phase 2 — Day 3 (3 November 2026): Application Factory and Database Foundation

The Flask entry point now initializes shared SQLAlchemy and Flask-Migrate
extensions through `create_app()`. The factory accepts an explicit
configuration, so tests use an isolated in-memory SQLite database while local
runs can use `DATABASE_URL` (or the local SQLite fallback).

The database models implement the Day 2 contract:

- `User`: unique username/email, password hash, constrained `user`/`admin` role.
- `Task`: required owner foreign key, title, description, status, priority and
  timestamps; status/priority/title checks and owner-oriented indexes.
- A one-to-many user/task relationship with cascading task deletion.

The initial Alembic revision is maintained in the repository-root `migrations/`
directory. From the repository root, install `python/requirements.txt`, set
`DATABASE_URL`, and run:

```bash
flask --app backend.app:app db upgrade
```

The database fixture creates and removes model metadata for isolated data
tests. A separate clean-database test runs `flask db upgrade` and verifies the
Alembic revision, tables, foreign key, and indexes. Run the focused tests with:

```bash
pytest projects/task-manager/tests/test_database.py
```

The `/health/database` endpoint performs a lightweight database connectivity
check. The Docker image runs Alembic migrations before Gunicorn starts; SQLite
is used for deterministic tests and does not replace PostgreSQL as the target
persistent database.
