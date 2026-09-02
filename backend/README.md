# Backend Development

This directory contains backend development concepts and Flask implementations covered throughout the Backend Engineer Roadmap.

The focus is on understanding how web applications work, building REST APIs with Flask, implementing authentication and authorization, and gradually moving toward production-oriented backend development.

---

## Topics

### HTTP Fundamentals

Covers the fundamentals of HTTP communication between clients and servers.

Topics include:

- HTTP requests
- HTTP responses
- HTTP methods
- Status codes
- Headers
- Request body
- Response body

---

### Flask Basics

Introduction to Flask and the basic structure of a Flask application.

Topics include:

- Flask application creation
- Routes
- Running the development server
- Request handling
- Response generation

---

### Flask Routing

Understanding how URLs are mapped to application functions.

Topics include:

- Route definitions
- URL parameters
- HTTP methods
- Route handlers

---

### REST APIs

Building APIs around REST principles.

Topics include:

- Resources
- HTTP methods
- Request and response formats
- Status codes
- CRUD operations

---

### Flask Blueprints

Organizing Flask applications into modular components using Blueprints.

Blueprints help separate application functionality into logical modules and make larger Flask applications easier to maintain.

## Day 19 — API Documentation

Day 19 introduces API documentation and OpenAPI concepts.

Topics include:

- API contracts
- OpenAPI specification
- Swagger
- Endpoint documentation
- Query parameters
- Path parameters
- Request bodies
- Request/response schemas
- HTTP status-code documentation

File:

`api_documentation.py`

The OpenAPI specification describes the API contract independently of the implementation.

This makes it easier for:

- Backend developers to understand endpoints
- Frontend developers to consume APIs
- Testers to understand expected behavior
- Teams to maintain consistent API contracts
- Documentation tools such as Swagger UI to render interactive API documentation

The repository currently uses a Python dictionary to model the OpenAPI document. It can later be exposed through an API endpoint and connected to Swagger UI.

---

### Request & Response Handling

Working with incoming requests and outgoing responses.

Topics include:

- Request data
- JSON payloads
- Query parameters
- Path parameters
- HTTP status codes
- JSON responses

---

### Error Handling

Handling application errors consistently.

Topics include:

- HTTP error responses
- Custom error handlers
- Validation errors
- Appropriate status codes
- Consistent API error responses

---

### Testing

Day 15 focus: Testing Flask applications with pytest.

Topics include:

- pytest-based Flask testing
- Flask test client
- Fixtures for Flask applications
- Testing request/response cycles
- API integration tests
- Status code assertions
- JSON response validation

**File:** `flask_testing.py`

---

# Authentication

Authentication answers:

> "Who is the user?"

The application verifies the identity of a user before allowing access to protected resources.

File:

`authentication.py`

Topics include:

- Authentication fundamentals
- User identity
- Password-based authentication
- Authentication flow
- Access control foundations

---

# Authorization

Authorization answers:

> "What is the authenticated user allowed to do?"

Authentication and authorization are separate concepts.

```text
Authentication
      ↓
Who are you?
      ↓
Authorization
      ↓
What are you allowed to do?
```

Topics include:

- Roles
- Permissions
- Role-Based Access Control (RBAC)
- Permission checks
- Resource ownership
- Access control

Authorization should be applied after the user has been authenticated.

File:

`authorization.py`

---

# JWT Authentication

JSON Web Tokens can be used to represent authenticated user identity between a client and backend service.

Topics include:

- JWT structure
- Access tokens
- Token generation
- Token validation
- Protected endpoints
- Token-based authentication

The Task Manager project implements JWT authentication incrementally.

---

# Logging

Logging records information about application execution and helps developers monitor, debug, and troubleshoot backend systems.

Day 13 introduces:

- Logging fundamentals
- Log levels
- Logger
- Handlers
- Formatters
- Exception logging
- Structured logging

File:

`logging_basics.py`

Common log levels include:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

Structured logs represent important event information in a consistent machine-readable format.

---

# Testing

Testing helps verify that backend logic behaves as expected and prevents regressions as the application grows.

Day 14 introduces:

- Unit tests
- Assertions
- Test functions
- Arrange / Act / Assert patterns
- Automated verification for backend behavior

File:

`testing_basics.py`

Testing is especially useful for:

- Authentication checks
- Authorization rules
- Request validation
- Business logic validation
- Route behavior

A project-level test suite is also being added to the Task Manager API to validate behavior as the roadmap advances.

---

# Flask Testing

Day 15 introduces testing Flask applications specifically.

Topics include:

- pytest-flask integration
- Test client for simulating requests
- Fixtures for Flask apps and clients
- Testing request/response cycles
- Mock testing patterns
- Status code assertions
- JSON response validation
- Error response handling
- Authentication header testing

File:

`flask_testing.py`

Flask testing allows you to:

- Test routes without running the server
- Simulate HTTP requests and responses
- Test error handling
- Validate response formats
- Test authentication and authorization
- Test edge cases and error conditions

---

## Day 18 — Standardized API Errors

Day 18 extends error handling into a consistent API error-response format.

The standard structure is:

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "The requested task was not found."
  }
}
```

The API uses appropriate HTTP status codes:

| Status code | Meaning |
|---|---|
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `409` | Conflict |
| `500` | Internal Server Error |

The goal is to avoid different endpoints returning inconsistent error formats.

---

# Day 20 — Flask Application Refactor

Day 20 introduces a production-oriented Flask application structure.

The main goals are:

- Application factory pattern
- Configuration separation
- Environment-specific configuration
- Blueprint registration
- Easier testing
- Better application organization

## Application Factory

The application is created through:

```python
create_app()
```

---

# Backend Learning Progress

Completed:

- HTTP Fundamentals
- Flask Basics
- Flask Routing
- REST APIs
- Flask Blueprints
- Request & Response Handling
- Error Handling
- Authentication Fundamentals
- Authorization
- JWT Authentication
- Logging Fundamentals
- Testing Basics

# Current focus:

- Task Manager validation
- Project-level automated testing

# Upcoming:

- Docker
- Deployment

---

## Learning Approach

For each backend topic:

1. Understand the underlying web concept.
2. Implement the concept using Flask or Python.
3. Build small API examples where appropriate.
4. Apply the concept to the Task Manager project when the roadmap assigns a project milestone.
5. Consider security and scalability implications.
6. Test the implementation.
7. Document the design and important decisions.

The goal is to gradually transform the Task Manager project from a basic Flask API into a production-style backend application.

---

# Day 22 —  Django Models, Migrations & Admin

Day 22 extends the Django fundamentals from Day 21 into database-backed
application development.

Topics include:

- Django models
- Model fields
- Model metadata
- Migrations
- Django admin
- Model registration
- URL Shortener domain modeling

File:

`django_models.py`

The repository's URL Shortener project also contains a Django model,
migration, and admin registration:

```text
projects/url-shortener/
├── admin.py
├── models.py
└── migrations/
    ├── __init__.py
    └── 0001_initial.py
```

The model represents a short URL and includes:

- Unique short code
- Original URL
- Creation timestamp
- Optional expiration timestamp
- Active/inactive state

Migrations provide version-controlled database schema changes derived from
the model definition.

---

# Day 23 — Django REST Framework Fundamentals

Day 23 introduces Django REST Framework (DRF) as the API layer on top of
Django.

Topics include:

- DRF fundamentals
- Serializers
- Input validation
- Representation of model-backed data
- API endpoint boundaries

File:

`django_rest_framework.py`

Serializers provide an explicit boundary between application data and API
representations. They can validate incoming data and control which fields are
returned to API clients.

The URL Shortener project applies these concepts through DRF serializers and
class-based API views.

---

# Day 24 — DRF ViewSets, Routers & Permissions

Day 24 builds on the DRF serializer and endpoint work from Day 23.

Topics include:

- DRF ViewSets
- Generic ViewSets and mixins
- Routers
- Permission classes
- Validation boundaries
- Consistent success response envelopes

File:

`django_rest_framework.py`

The URL Shortener project applies the same concepts through a router-registered
ViewSet with explicit read/write permission behavior.

---

# Day 25 — Django Authentication, Sessions & Permissions

Day 25 adds Django's built-in authentication model to the backend roadmap.

Topics include:

- Credential authentication
- Session-based login/logout
- `login_required` boundaries
- Permission checks
- Authenticated ownership of project resources

File:

`django_authentication.py`

The URL Shortener project uses the authenticated Django user as the owner of
new short URLs and restricts API access to authenticated users.

---

## Day 26 — FastAPI Fundamentals

Day 26 introduces FastAPI as the next backend framework in the roadmap and
compares its request handling model with the Django/DRF work from Days 21–25.

Topics include:

- FastAPI application setup
- Route declarations
- Path and query parameters
- Dependency injection with `Depends`
- Automatic API schema generation
- Lightweight, function-oriented endpoint definitions

File:

`fastapi_fundamentals.py`

The URL Shortener project also contains a small FastAPI implementation so the
framework can be compared against the existing Django/DRF version without
removing the earlier work.

---

## Day 27 — FastAPI Validation & Response Models

Day 27 extends the FastAPI foundation with explicit validation, response
contracts, and reusable dependencies.

Topics include:

- Pydantic request models
- Field constraints
- Path and query parameter validation
- Response models
- `Depends`
- Dependency-injected request context and storage
- Automatic API schema generation

Files:

- `fastapi_validation_response_models.py`
- `fastapi_fundamentals.py`

The URL Shortener FastAPI comparison implementation also applies these patterns
to a small project-level API.

---

## Day 28 — FastAPI Authentication with OAuth2 & JWT

Day 28 introduces authentication patterns for FastAPI applications.

Topics include:

- OAuth2 bearer-token concepts
- `OAuth2PasswordBearer`
- JWT access tokens
- Token expiration and validation
- Authentication vs authorization
- Protecting endpoints with FastAPI dependencies
- `401 Unauthorized` responses and the `WWW-Authenticate` header

File:

`fastapi_authentication.py`

The example focuses on the authentication boundary. Authorization decisions
such as roles and permissions remain a separate concern.

---

## Day 29 — FastAPI API Testing

Day 29 focuses on testing FastAPI endpoints as an HTTP API rather than testing
only individual functions.

Topics include:

- FastAPI `TestClient`
- Request and response assertions
- Request validation testing
- HTTP error response testing
- Dependency overrides
- Isolated test state
- Testing async endpoints through the API boundary

File:

`fastapi_testing.py`

The URL Shortener project contains the complete project-level API test suite
under `projects/url-shortener/tests/`.

---

## Day 30 — Flask vs Django vs FastAPI

Day 30 reviews the backend frameworks used throughout the roadmap and focuses
on choosing the right tool for a given service.

### Framework Comparison

| Area | Flask | Django / DRF | FastAPI |
|---|---|---|---|
| Core approach | Lightweight WSGI framework | Full-stack framework + REST toolkit | API-focused ASGI framework |
| Best fit | Small services and custom applications | Feature-rich applications with ORM/admin/auth needs | Typed APIs and async-friendly services |
| ORM | External choice | Django ORM | External choice |
| Validation | Extension/application layer | DRF serializers | Pydantic / FastAPI validation |
| API schema | Extension/tooling | DRF/OpenAPI tooling | Automatic OpenAPI support |
| Async model | Possible with supporting stack | Django supports async patterns | First-class async endpoint model |
| Batteries included | Low | High | Focused on APIs |
| Main trade-off | More components are chosen separately | Larger framework surface | API-centric rather than full-stack |

### Selection Checklist

Choose based on:

1. Application scope and complexity.
2. Existing team and project conventions.
3. ORM, admin, and authentication requirements.
4. Async I/O requirements.
5. Validation and type-safety needs.
6. Deployment and operational constraints.
7. Long-term maintainability.

File:

`framework_comparison.py`

---

## Day 31 — Database Connection Pooling

Day 31 introduces database connection pooling as a backend resource-management
concern.

Topics include:

- Reusing database connections
- Bounded connection pools
- Borrowing and returning connections
- Pool exhaustion
- Connection leaks
- Long-running transactions
- Pool sizing across multiple application instances

File:

`connection_pooling.py`

The example uses a small standard-library pool abstraction so the lifecycle can
be studied without requiring a specific database driver.

---

## Day 32 — SQLAlchemy / ORM Session Concepts

Day 32 introduces SQLAlchemy 2.x ORM session patterns for database-backed
backend services.

Topics include:

- Declarative ORM models
- `Session` lifecycle
- Adding and querying ORM entities
- Explicit commit and rollback
- Flush and refresh behavior
- Keeping transaction ownership explicit

File:

`sqlalchemy_session.py`

The example uses a small Expense model and a local SQLite database so the ORM
session lifecycle can be studied without requiring an external database.

---

## Day 33 — Background Jobs

Day 33 introduces background jobs as a way to move work that does not need to
complete in the request path into asynchronous processing.

Topics include:

- Background job boundaries
- Producer and worker responsibilities
- In-process job queues
- Job lifecycle
- Waiting for completion during controlled shutdown
- Separating request latency from background work
- When a durable external queue is preferable

File:

`background_jobs.py`

The example uses the standard library to demonstrate the application-side
producer/worker boundary without introducing a third-party task framework.
