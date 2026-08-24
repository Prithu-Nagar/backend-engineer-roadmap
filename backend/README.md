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

### Day 18 — Standardized API Errors

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
