# Task Manager REST API

A backend API developed incrementally as part of the Backend Engineer Roadmap.

The project is being built progressively to apply backend concepts learned throughout the roadmap.

---

## Current Status

The Task Manager API currently demonstrates basic Flask routing, request/response handling, validation, HTTP status codes, and JSON responses.

---

## Day 8

Added request and response handling to the Task Manager API.

### Implemented

* Path parameters
* Query parameters
* JSON request bodies
* Basic request validation
* HTTP status codes
* JSON responses
* Flask Blueprint-based routing

---

## Endpoints

| Method | Endpoint                      | Purpose                  |
| ------ | ----------------------------- | ------------------------ |
| GET    | `/api/tasks/`                 | Retrieve tasks           |
| GET    | `/api/tasks/<task_id>`        | Retrieve a specific task |
| GET    | `/api/tasks/search?query=...` | Search tasks             |
| POST   | `/api/tasks/`                 | Create a task            |

PUT and DELETE operations are planned for a future iteration.

---

## Request Flow

Client
  ↓
HTTP Request
  ↓
Flask Application
  ↓
Task Manager Blueprint
  ↓
Request Data
  ↓
Validation
  ↓
Response

---

## Implementation

The Task Manager API implementation is currently located in the repository's `backend/` directory.

Relevant files include:

* `backend/app.py`
* `backend/flask_routing.py`
* `backend/request_response.py`

The standalone request/response examples are demonstrated in `backend/request_response.py`, while the Task Manager routes are implemented through the Blueprint in `backend/flask_routing.py`.

---

## API Structure

The Task Manager Blueprint uses the following base path:

/api/tasks

This keeps the Task Manager endpoints grouped under a dedicated API namespace.

---

## Roadmap

Future iterations will introduce:

* Persistent database storage
* PUT and DELETE operations
* Automated testing
* Authentication
* Authorization
* Logging
* Production-oriented infrastructure
