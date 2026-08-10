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

## Planned Enhancements

- SQLite Integration
- SQLAlchemy
- Service Layer
- Request Validation
- JWT
- Testing
- Logging
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
- Authentication
- Authorization
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
