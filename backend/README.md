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

# Authentication

Authentication answers:

"Who is the user?"

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

"What is the authenticated user allowed to do?"

Authentication and authorization are separate concepts.

Authentication
      ↓
Who are you?
      ↓
Authorization
      ↓
What are you allowed to do?

Day 12 introduces:

Roles
Permissions
Role-Based Access Control (RBAC)
Permission checks
Resource ownership
Access control

Authorization should be applied after the user has been authenticated.

File:

`authorization.py`

# JWT Authentication

JSON Web Tokens can be used to represent authenticated user identity between a client and backend service.

Topics include:

JWT structure
Access tokens
Token generation
Token validation
Protected endpoints
Token-based authentication

The Task Manager project implements JWT authentication incrementally.

Authentication vs Authorization
Concept	Purpose
Authentication	Verifies user identity
Authorization	Determines allowed actions
Role	Groups permissions
Permission	Represents an allowed operation

Example:

User logs in
    ↓
Authentication
    ↓
JWT issued
    ↓
Request contains JWT
    ↓
JWT validated
    ↓
User identity established
    ↓
Authorization check
    ↓
Permission granted or denied
Role-Based Access Control

RBAC assigns permissions to roles.

Example:

Admin
 ├── create_task
 ├── read_task
 ├── update_task
 ├── delete_task
 └── manage_users

User
 ├── create_task
 ├── read_task
 ├── update_task
 └── delete_task

This allows authorization rules to be managed through roles instead of checking individual users throughout the application.

Authorization Responses

A backend should distinguish between authentication and authorization failures.

401 Unauthorized

Used when authentication is required or the provided authentication credentials are invalid.

403 Forbidden

Used when the user is authenticated but does not have permission to perform the requested action.

Example:

Unauthenticated request
        ↓
       401

Authenticated but insufficient permission
        ↓
       403
Backend Learning Progress

File:

`jwt_authentication.py`

Completed:

HTTP Fundamentals
Flask Basics
Flask Routing
REST APIs
Flask Blueprints
Request & Response Handling
Error Handling
Authentication Fundamentals

Current focus:

Authorization
JWT Authentication

Upcoming:

Logging
Testing
Docker
Deployment
Learning Approach

For each backend topic:

Understand the underlying web concept.
Implement the concept using Flask.
Build small API examples.
Apply the concept to the Task Manager project.
Consider security and scalability implications.
Test the implementation.
Document the design and important decisions.

The goal is to gradually transform the Task Manager project from a basic Flask API into a production-style backend application.
