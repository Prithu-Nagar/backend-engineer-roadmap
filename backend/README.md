# Backend

This directory contains Flask-based backend development examples and the Task Manager API implementation.

---

## Completed Topics

- HTTP Fundamentals
- Flask Basics
- Flask Routing
- REST APIs
- Flask Blueprints
- Request & Response Handling

---

## Repository Files

backend/
├── README.md
├── app.py
├── flask_basics.py
├── flask_routing.py
└── request_response.py

---

## Flask Application

The Task Manager API is initialized in:

`app.py`

The Flask Blueprint and Task Manager routes are implemented in:

`flask_routing.py`

---

## Request & Response Handling

The repository demonstrates:

- Path parameters
- Query parameters
- JSON request bodies
- Basic request validation
- HTTP status codes
- JSON responses

The standalone examples are available in:

`request_response.py`

The concepts are also integrated into the Task Manager routes in:

`flask_routing.py`

---

## Current API

The Task Manager currently supports:

| Method |          Endpoint             |      Purpose        |
|--------|-------------------------------|---------------------|
| GET    | `/api/tasks/`                 | Get tasks           |
| GET    | `/api/tasks/<task_id>`        | Get a specific task |
| GET    | `/api/tasks/search?query=...` | Search tasks        |
| POST   | `/api/tasks/`                 | Create a task       |

PUT and DELETE operations will be introduced in a later iteration.

---

## Upcoming Topics

- Authentication
- JWT
- Logging
- Testing
- FastAPI
- Django
- Docker
- Deployment
