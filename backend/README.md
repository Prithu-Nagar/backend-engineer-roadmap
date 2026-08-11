# Backend

This directory contains practical backend development examples using Flask, with a focus on HTTP, routing, REST APIs, request/response handling, error handling, authentication, and modular application structure.

---

# Topics

## Flask Basics

Covers creating Flask applications, defining routes, handling requests, and returning responses.

File: `flask_basics.py`

---

## Flask Routing

Covers Flask routing and the Task Manager API structure.

Topics include:

- Flask routes
- Dynamic path parameters
- Query parameters
- HTTP methods
- JSON request bodies
- Basic request validation
- HTTP status codes
- Flask Blueprints

File: `flask_routing.py`

---

## Request & Response Handling

Covers handling incoming HTTP requests and constructing appropriate responses.

Topics include:

- Path parameters
- Query parameters
- JSON request bodies
- Request validation
- HTTP status codes
- JSON responses

File: `request_response.py`

---

## Error Handling

Covers handling invalid requests and application errors in Flask.

Topics include:

- HTTP 400 Bad Request
- HTTP 404 Not Found
- HTTP 500 Internal Server Error
- JSON error responses
- Flask error handlers

File: `error_handling.py`

---

## Authentication

Covers the basic authentication flow for protecting backend endpoints.

Topics include:

- Authentication vs authorization
- Password hashing
- Password verification
- HTTP Basic Authentication
- Protected endpoints
- Authentication decorators
- `401 Unauthorized`
- `WWW-Authenticate` response headers

File: `authentication.py`

The example uses Werkzeug's password hashing utilities instead of storing plaintext passwords.

> This is a learning example. Production applications should use a proper authentication architecture, secure secret management, HTTPS, appropriate session or token management, and additional security controls.

---

## JWT Authentication

JSON Web Tokens (JWT) can be used to authenticate requests to protected backend resources.

A typical authentication flow is:

Client
   |
   | Login credentials
   v
Backend
   |
   | Validate credentials
   v
Generate JWT
   |
   v
Client
   |
   | Authorization: Bearer <token>
   v
Protected Endpoint

A JWT commonly contains:

Subject (sub)
Issued-at time (iat)
Expiration time (exp)

The backend validates the token before allowing access to protected resources.

Access Token

An access token represents the authenticated user's session or authorization context.

The client sends the token using the HTTP Authorization header:

Authorization: Bearer <token>
Token Validation

The backend should:

Extract the token.
Verify its signature.
Verify that it has not expired.
Read the relevant claims.
Continue only when the token is valid.

Authentication answers:

Who is the user?

Authorization answers:

What is the user allowed to do?

JWT is therefore primarily an authentication mechanism, while authorization rules determine what authenticated users can access.

---

# Main Application

The Task Manager API application is initialized through:

`app.py`

The application registers the Task Manager Blueprint defined in `flask_routing.py`.

---

# Repository Structure

backend/
├── README.md
├── app.py
├── authentication.py
├── error_handling.py
├── flask_basics.py
├── flask_routing.py
└── request_response.py

---

# Completed Topics

- Flask Basics
- Flask Routing
- Request & Response Handling
- Error Handling
- Authentication Fundamentals

---

# Upcoming Topics

- JWT
- Authorization
- Logging
- Testing
- FastAPI
- Django
- Docker
- Deployment

---

# Learning Approach

For each backend topic:

1. Understand the underlying web or framework concept.
2. Implement a small practical example.
3. Follow HTTP and REST conventions.
4. Handle successful and unsuccessful requests appropriately.
5. Keep application structure modular and maintainable.
6. Apply the concepts progressively to backend projects.
