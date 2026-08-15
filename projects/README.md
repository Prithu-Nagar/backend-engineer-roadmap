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
├── app.py
├── flask_basics.py
├── flask_routing.py
├── authentication.py
├── authorization.py ← NEW
├── error_handling.py
├── jwt_authentication.py
└── request_response.py

The long-term direction is:

Client
   ↓
Flask Application
   ↓
Routes / Blueprints
   ↓
Service Layer
   ↓
Database / Models

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
