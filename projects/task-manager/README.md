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

The current authentication and authorization flow is:

Client
   ↓
Login
   ↓
Authentication
   ↓
JWT Access Token
   ↓
Authenticated Request
   ↓
JWT Validation
   ↓
Authorization
   ↓
Role / Permission Check
   ↓
Task Resource

Authentication determines who the user is.

Authorization determines what the authenticated user is allowed to do.

Features
Task Management

The project demonstrates authorization rules for:

- Create task
- Read task
- Update task
- Delete task

The underlying REST API endpoints for PUT and DELETE will be implemented as the project evolves.

Authentication verifies the identity of the user.

The project has progressively introduced:

Authentication fundamentals
User identity
Password verification
JWT access tokens
Token validation

JWT tokens contain information required to identify the authenticated user.

JWT Authentication

The authentication flow is:

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

The JWT contains user-related claims such as:

User ID
Username
Role
Issued-at time
Expiration time
Authorization

Authorization is performed after authentication.

The project uses role-based authorization.

Example roles:

Admin
User

Permissions are associated with roles.

Example:

Admin
 ├── create_task
 ├── read_task
 ├── update_task
 ├── delete_task
 └── manage_users

User
 ├── create_task
 ├── read_task
 ├── update_task
 └── delete_task
Role-Based Access Control

RBAC allows permissions to be associated with roles rather than implementing separate authorization rules for every user.

The basic flow is:

Authenticated User
        ↓
      Role
        ↓
   Permissions
        ↓
Permission Check
        ↓
Allow / Deny

For example, an administrator can access user-management functionality while a normal user cannot.

Resource Authorization

Authorization can also depend on resource ownership.

For example:

User A
   ↓
Owns Task 1
   ↓
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
        ↓
       401

Authenticated
      ↓
Permission check
      ↓
Permission denied
      ↓
       403
Project Structure

The project is being expanded incrementally as new backend concepts are introduced.

Relevant authentication and authorization files include:

projects/
└── task-manager/
    ├── README.md
    └── jwt_authentication.py

Backend-level authentication and authorization implementations are maintained separately from the project-specific implementation.

Development Strategy

The Task Manager follows the same incremental approach as the roadmap.

Each major concept is first learned independently and then applied to the project.

Example progression:

Flask Basics
      ↓
Routing
      ↓
REST API
      ↓
CRUD
      ↓
Request / Response Handling
      ↓
Error Handling
      ↓
Authentication
      ↓
JWT
      ↓
Authorization
      ↓
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

Current focus:

Applying authorization rules to task operations
Separating authentication from authorization
Enforcing role and permission checks
Logging application events
Adding automated tests for auth and authorization behavior

Relevant files:

- `logging_config.py`
- `tests/test_task_manager.py`

---

## Testing (Day 15)

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

## API Validation and Schemas (Day 16)

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

## Pagination, Filtering and Sorting (Day 17)

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

# Day 18 — Standardized Errors + Generators

Day 18 extends the Task Manager with:

- Consistent API error responses
- Standard error codes
- HTTP status-code conventions
- Generator-based task processing
- Lazy evaluation
- Generator pipelines

## Standard Error Format

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
  ↓
Task Generator
  ↓
Completion Filter
  ↓
Priority Filter
  ↓
Result

The generator pipeline avoids creating unnecessary intermediate lists
and demonstrates lazy evaluation in the project.

Day 18 Files
error_handling.py
generators.py
tests/test_error_handling.py
tests/test_generators.py

---

## Test Approach

Tests follow the Arrange-Act-Assert pattern:

1. Arrange — Set up test data and fixtures
2. Act — Execute the operation being tested
3. Assert — Verify the results

---

## Future Improvements

Planned improvements include:

Database persistence
Better password hashing
Token refresh mechanism
More granular permissions
Dockerization
Production deployment
Improved configuration management
API documentation

The project will continue evolving as new backend, system-design, SQL, and Python concepts are introduced throughout the roadmap.
