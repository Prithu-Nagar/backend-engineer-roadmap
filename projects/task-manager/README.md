# Task Manager REST API

A backend REST API built incrementally as part of the Backend Engineer Roadmap.

The project is being developed alongside the roadmap so that concepts learned in DSA, Python, backend development, SQL, and system design can be applied to a practical backend application.

---

## Current Features

The API currently covers:

- Flask application setup
- REST API structure
- Routing
- Request handling
- Response handling
- JSON responses
- CRUD operations
- Error handling
- Blueprint-based application structure
- Authentication fundamentals

---

## Architecture

The application follows a modular Flask architecture.

Client
  |
  v
Flask Application
  |
  v
Blueprint / Routes
  |
  +----> Request Validation
  |
  +----> Authentication
  |
  +----> Authorization
  |
  v
Business Logic
  |
  v
Database

The goal is to keep request handling, authentication, business logic, and persistence responsibilities separated as the project grows.

---

## API Flow

A protected request follows this general flow:

Client
  |
  | HTTP Request
  v
Flask Route
  |
  v
Authentication
  |
  v
Authorization
  |
  v
Request Validation
  |
  v
Business Logic
  |
  v
Database
  |
  v
HTTP Response

Authentication establishes the identity of the caller.

Authorization determines whether that caller is allowed to access or modify the requested resource.

---

## Authentication

Authentication is responsible for verifying the identity of a user before allowing access to protected resources.

The current roadmap implementation demonstrates:

- Password hashing
- Password verification
- Basic authentication
- Protected Flask endpoints
- Authentication decorators
- `401 Unauthorized` responses

The standalone authentication example is available at:

`backend/authentication.py`

This project documentation establishes the architectural direction for integrating authentication into the Task Manager API.

---

## Authorization

Authentication alone is not sufficient.

For example, if user `A` requests:

GET /tasks/15

the application must determine whether task `15` belongs to user `A` or whether the user otherwise has permission to access it.

Authorization should therefore happen before returning protected resources.

A future implementation can introduce:

- User identity
- Resource ownership
- Roles
- Permissions
- Role-based access control

---

## Security Principles

The API should follow these principles as authentication is integrated:

- Never store plaintext passwords.
- Use HTTPS in production.
- Validate incoming requests.
- Authenticate protected requests.
- Authorize access to resources.
- Follow least-privilege principles.
- Keep secrets outside source control.
- Return appropriate HTTP status codes.
- Avoid exposing sensitive internal errors.
- Log security-relevant events appropriately.

---

## Example Protected Request

GET /tasks/15
Authorization: Bearer <access-token>

The application should:

1. Receive the request.
2. Validate the authentication credential.
3. Identify the user.
4. Check whether the user can access task 15.
5. Retrieve the task.
6. Return the appropriate response.

The client should never be trusted to enforce authorization by itself.

---

## Current API Direction

The Task Manager API is being developed incrementally.

Current architectural priorities are:

1. HTTP fundamentals
2. REST API design
3. CRUD operations
4. Request and response handling
5. Error handling
6. Authentication
7. Authorization
8. Database integration
9. Testing
10. Deployment

---

## Future Improvements

Planned improvements include:

- User management
- JWT-based authentication
- Role-based authorization
- Persistent database storage
- Request validation
- Automated tests
- Logging
- Dockerization
- API documentation
- Production deployment

---

## Learning Purpose

This project is intentionally developed incrementally rather than as a single large application.

Each roadmap milestone introduces another production-relevant backend concept while keeping the application understandable and maintainable.

