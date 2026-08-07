# Backend

This directory contains backend development concepts, Flask applications, and REST API implementations built during the Backend Engineer Roadmap.

---

## Completed

### HTTP Fundamentals

- HTTP Methods
- HTTP Status Codes
- Request & Response
- Headers
- URL Parameters
- Query Parameters

### Flask Basics

Files

- app.py
- flask_basics.py

Topics Covered

- Creating a Flask Application
- Running a Flask Server
- Routes
- Dynamic Routes
- URL Parameters
- JSON Responses
- Request Object
- HTTP Methods
- Debug Mode

---

### Flask Routing

Files

- flask_routing.py

Topics Covered

- Static Routes
- Dynamic Routes
- Variable Rules
- Route Converters
- Multiple Routes
- URL Building
- Route Methods (GET & POST)

---

### REST APIs

Topics Covered

- REST Architecture
- REST Constraints
- Resources
- CRUD Operations
- REST URL Design
- GET Endpoint
- POST Endpoint
- PUT Endpoint
- DELETE Endpoint
- JSON Request Body
- JSON Response
- Route Parameters
- Flask Blueprints

---

### Flask Blueprints

Flask Blueprints provide a way to organize routes into modular components.

The Task Manager API uses a Blueprint for task-related routes.

task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/api/tasks"
)

---

## Learning Approach

The backend module is organized progressively.

Concepts are first implemented in small standalone examples to understand the fundamentals. Once understood, they are integrated into the main Task Manager API (`app.py`), allowing the project to evolve into a more complete backend application over time.

## Upcoming

- SQLAlchemy
- Authentication
- JWT
- Validation
- Logging
- Testing
- FastAPI
- Django
- Docker
- Deployment