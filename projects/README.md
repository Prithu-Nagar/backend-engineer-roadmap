# Projects

This directory contains end-to-end backend projects built throughout the roadmap.

The projects are developed incrementally alongside the topics covered in the roadmap.

---

## Current Project

### Task Manager REST API

**Status:** 🚧 In Progress

The Task Manager REST API is the primary backend project being developed throughout the roadmap.

Instead of creating multiple small projects, the same application evolves over time by incorporating newly learned backend concepts.

---

## Current Technology Stack

- Python
- Flask
- Django
- Django REST Framework
- FastAPI
- REST APIs

---

## Current Features

### Flask Application

- Flask application setup
- Basic routing
- JSON responses
- HTTP methods
- Route parameters
- Query parameters
- Flask Blueprints
- Request validation
- Structured logging configuration
- Basic automated testing

### REST API

The current API supports basic task retrieval and creation.

|Method |          Endpoint             |        Purpose      |
|-------|-------------------------------|---------------------|
| GET   | `/api/tasks/`                 | Get tasks           |
| GET   | `/api/tasks/<task_id>`        | Get a specific task |
| GET   | `/api/tasks/search?query=...` | Search tasks        |
| POST  | `/api/tasks/`                 | Create a task       |

PUT and DELETE operations have not been implemented yet.

---

## Flask Routing

Flask routing concepts are also being explored separately as the project architecture evolves.

Current routing concepts include:

- Static routes
- Dynamic routes
- Route parameters
- Query parameters
- GET endpoints
- POST endpoints
- JSON responses
- Flask Blueprints

The Blueprint is implemented in:

`backend/flask_routing.py`

The main Task Manager application is initialized in:

`backend/app.py`

---

## Current Architecture

The project is currently evolving from a simple Flask application toward a more modular backend architecture.

Current structure:

backend/
```text
├── app.py
├── flask_basics.py
├── flask_routing.py
├── authentication.py
├── authorization.py ← NEW
├── error_handling.py
├── jwt_authentication.py
└── request_response.py
```

The long-term direction is:

```text
Client
   ↓
```
Flask Application
```text
   ↓
```
Routes / Blueprints
```text
   ↓
Service Layer
   ↓
Database / Models

```
The service and database layers will be introduced as the project progresses through the roadmap.

---

Current authentication/authorization concepts:

- JWT authentication
- Authorization
- Role-Based Access Control
- Permissions
- Resource ownership

---

## Testing

Day 15 introduces comprehensive testing for the Task Manager API.

Testing implementation includes:

- pytest-flask integration
- Fixtures for Flask applications
- Test client for simulating HTTP requests
- Authentication and authorization tests
- Task operation tests
- Permission and access control tests
- Test configuration with `conftest.py`

Test files:

- `tests/conftest.py` — Pytest fixtures and configuration
- `tests/test_tasks.py` — Task CRUD operations and filtering tests
- `tests/test_auth.py` — Authentication, authorization, and token tests

The tests serve as both verification and documentation of API behavior.

---

### Day 18

The Task Manager now includes:

- Standardized API error responses
- Error codes
- Consistent HTTP status handling
- Generator-based task processing
- Lazy task pipelines
- Generator-based filtering

---

## Day 22 — URL Shortener Django Model

The URL Shortener project now moves from requirements/schema work into
Django-backed domain modeling.

Added:

- `projects/url-shortener/models.py`
- `projects/url-shortener/admin.py`
- `projects/url-shortener/migrations/0001_initial.py`

The `ShortURL` model contains:

- `short_code`
- `original_url`
- `created_at`
- `expires_at`
- `is_active`

The initial migration captures the database schema represented by the Django
model, while the admin registration provides a basic administrative interface
for inspecting and managing short URLs.

---

## Day 23 — URL Shortener DRF API

The URL Shortener now moves from Django persistence into its first API layer.

Added:

- `projects/url-shortener/serializers.py`
- `projects/url-shortener/views.py`
- `projects/url-shortener/urls.py`

The DRF layer provides list/create and detail endpoints for active short URLs.
Serializers define the API representation while generic DRF views handle the
request/response flow.

---

## Planned Enhancements

- SQLite Integration
- SQLAlchemy
- Service Layer
- Request Validation
- Testing
- Docker
- Deployment

---

## Future API Improvements

Future iterations will introduce:

- PUT and DELETE operations
- Persistent database storage
- Database models
- Improved validation
- Consistent error responses
- Automated tests
- API documentation

---

## Planned Projects

- URL Shortener
- Expense Tracker API
- Blog API
- Chat Application

---

## Development Philosophy

This project grows alongside the roadmap.

Each new backend concept is integrated into the existing application where appropriate instead of creating separate demo projects.

The goal is to gradually transform the initial Flask application into a production-oriented backend service while maintaining clean code and clear separation of responsibilities.

---

## Day 24 — URL Shortener Validation + API Responses

The URL Shortener now adds a stronger API boundary around the DRF layer.

Added or updated:

- Serializer validation for URLs and expiration timestamps
- Server-generated unique short codes
- DRF ViewSet structure
- Router-based URL registration
- Permission classes
- Consistent success response envelopes

The implementation remains limited to the roadmap's current list/create/detail
API scope rather than pulling future authentication and administration work
forward.


## Day 25 — URL Shortener Authentication & Admin

The URL Shortener now introduces authenticated ownership.

Added or updated:

- `projects/url-shortener/permissions.py`
- `projects/url-shortener/migrations/0002_shorturl_owner.py`
- Owner field on `ShortURL`
- Authenticated DRF access
- Owner-scoped URL listing and retrieval
- Django admin ownership visibility

New short URLs are associated with the authenticated Django user. 

---

## Day 26 — URL Shortener FastAPI Comparison

Day 26 adds a small FastAPI implementation of the URL Shortener alongside the
existing Django/DRF version. The goal is framework comparison, not replacement
of the existing project implementation.

Added:

- `projects/url-shortener/fastapi_app.py`

The comparison implementation demonstrates:

- FastAPI application and route declarations
- Request validation with Pydantic models
- Response models
- Dependency injection
- Create, list, and retrieve URL endpoints
- Explicit HTTP error responses

The FastAPI version uses an in-memory store intentionally. The existing Django
model, migrations, authentication, ownership, and DRF implementation remain the
source of truth for the project's persistent implementation at this stage.

---

## Day 27 — URL Shortener FastAPI Validation & Dependency Injection

Day 27 extends the FastAPI comparison implementation with stronger request and
response contracts and reusable dependencies.

Updated:

- `projects/url-shortener/fastapi_app.py`

The implementation demonstrates:

- Pydantic request validation
- Response models
- Header-based request context
- Dependency injection with `Depends`
- Injected storage access
- Explicit HTTP error responses

The Django/DRF implementation remains the persistent project source of truth;
the FastAPI implementation continues to serve as a framework comparison and
learning artifact.

---

## Day 28 — URL Shortener Async Endpoint

The URL Shortener FastAPI comparison now includes an asynchronous endpoint.

Updated:

- `projects/url-shortener/fastapi_app.py`

The FastAPI list endpoint is now declared with `async def` and yields to the
event loop before returning the in-memory collection. This keeps the project
aligned with the day's async FastAPI focus without replacing the existing
Django/DRF implementation.

---

## Day 29 — URL Shortener Complete Test Suite

Day 29 completes the FastAPI comparison testing layer for the URL Shortener.

Added:

- `projects/url-shortener/tests/conftest.py`
- `projects/url-shortener/tests/test_fastapi_app.py`
- `projects/url-shortener/tests/__init__.py`

The test suite covers:

- FastAPI `TestClient`
- Dependency overrides
- Isolated in-memory stores
- Successful URL creation
- Request validation
- URL listing
- URL retrieval
- `404 Not Found` behavior

The existing Django/DRF implementation and all earlier project work remain
unchanged.

---

## Day 30 — URL Shortener Milestone + README

Day 30 consolidates the URL Shortener work completed during Days 21–29.

Milestone review:

- Django/DRF project structure
- URL model and migrations
- Serializer validation and API responses
- ViewSets, routers, and permissions
- Authentication and ownership
- FastAPI comparison implementation
- Async FastAPI endpoint
- API testing with dependency overrides
- Backward-compatible migration practices

The project README is updated as the phase checkpoint. No new application
feature is introduced on Day 30; the milestone focuses on consolidation,
documentation, and readiness for the database/distributed-systems phase.

## Day 31 — Expense Tracker Requirements

Day 31 starts the Expense Tracker project for the Databases & Distributed
Systems phase.

Added:

- `projects/expense-tracker/README.md`

The requirements define:

- Expense creation
- Expense listing and filtering
- Date-range queries
- Pagination
- Expense retrieval, update, and deletion
- Relational data requirements
- Validation and HTTP expectations
- Transaction and connection-pooling considerations

Day 31 intentionally defines the project boundary without implementing the
database schema or CRUD layer. Those implementation steps are scheduled for
Day 32.
