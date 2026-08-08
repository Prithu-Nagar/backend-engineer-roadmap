# Task Manager REST API

A backend API developed incrementally as part of the Backend Engineer Roadmap.

## Day 8

Added request and response handling to the Task Manager API.

### Implemented

- Path parameters
- Query parameters
- JSON request bodies
- Basic request validation
- HTTP status codes
- JSON responses

## Endpoints

| Method |          Endpoint             |        Purpose           |
|--------|-------------------------------|--------------------------|
| GET    | `/api/tasks/`                 | Retrieve tasks           |
| GET    | `/api/tasks/<task_id>`        | Retrieve a specific task |
| GET    | `/api/tasks/search?query=...` | Search tasks             |
| POST   | `/api/tasks/`                 | Create a task            |

PUT and DELETE operations are planned for a future iteration.

## Request Flow

Client
  ↓
HTTP Request
  ↓
Flask Blueprint
  ↓
Request Data
  ↓
Validation
  ↓
Business Logic
  ↓
HTTP Response

## Project Structure

backend/
├── app.py
├── flask_basics.py
├── flask_routing.py
└── request_response.py

The request/response concepts are demonstrated in `request_response.py` and integrated into the Task Manager routes in `flask_routing.py`.

## Roadmap

Future iterations will introduce persistent storage, automated testing, authentication, and production-oriented infrastructure.
