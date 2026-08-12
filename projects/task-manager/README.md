# Task Manager REST API

The Task Manager is the primary backend project for the Backend Engineer Roadmap.

The project is being developed incrementally alongside the roadmap so that concepts learned each day are applied to a realistic backend application.

---

## Project Goals

The Task Manager API is designed to demonstrate:

- REST API development
- Flask application structure
- CRUD operations
- Request and response handling
- Error handling
- Authentication
- JWT authentication
- Authorization
- Role-Based Access Control (RBAC)
- Database integration
- API security
- Production-oriented backend design

---

# Current Architecture

The project is being developed incrementally.

The current authentication and authorization flow is:

Client
   ↓
Login
   ↓
Authentication
   ↓
JWT Access Token
   ↓
Authenticated Request
   ↓
JWT Validation
   ↓
Authorization
   ↓
Role / Permission Check
   ↓
Task Resource

Authentication determines who the user is.

Authorization determines what the authenticated user is allowed to do.

Features
Task Management

The project demonstrates authorization rules for:

- Create task
- Read task
- Update task
- Delete task

The underlying REST API endpoints for PUT and DELETE will be implemented as the project evolves.

Authentication verifies the identity of the user.

The project has progressively introduced:

Authentication fundamentals
User identity
Password verification
JWT access tokens
Token validation

JWT tokens contain information required to identify the authenticated user.

JWT Authentication

The authentication flow is:

User
 ↓
Login Request
 ↓
Verify Credentials
 ↓
Create JWT
 ↓
Return Access Token
 ↓
Client Stores Token
 ↓
Client Sends Token
 ↓
Backend Validates JWT
 ↓
Authenticated User

The JWT contains user-related claims such as:

User ID
Username
Role
Issued-at time
Expiration time
Authorization

Authorization is performed after authentication.

The project uses role-based authorization.

Example roles:

Admin
User

Permissions are associated with roles.

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
Role-Based Access Control

RBAC allows permissions to be associated with roles rather than implementing separate authorization rules for every user.

The basic flow is:

Authenticated User
        ↓
      Role
        ↓
   Permissions
        ↓
Permission Check
        ↓
Allow / Deny

For example, an administrator can access user-management functionality while a normal user cannot.

Resource Authorization

Authorization can also depend on resource ownership.

For example:

User A
   ↓
Owns Task 1
   ↓
Can access Task 1

A normal user should not automatically be allowed to modify another user's task.

An administrator can be granted broader access.

Therefore, authorization can involve both:

Role permissions
Resource ownership
HTTP Authorization Responses

The project distinguishes between authentication and authorization failures.

401 Unauthorized

Returned when authentication is required but the user has not successfully authenticated.

403 Forbidden

Returned when the user is authenticated but does not have permission to perform the requested operation.

Example:

No valid authentication
        ↓
       401

Authenticated
      ↓
Permission check
      ↓
Permission denied
      ↓
       403
Project Structure

The project is being expanded incrementally as new backend concepts are introduced.

Relevant authentication and authorization files include:

projects/
└── task-manager/
    ├── README.md
    └── jwt_authentication.py

Backend-level authentication and authorization implementations are maintained separately from the project-specific implementation.

Development Strategy

The Task Manager follows the same incremental approach as the roadmap.

Each major concept is first learned independently and then applied to the project.

Example progression:

Flask Basics
      ↓
Routing
      ↓
REST API
      ↓
CRUD
      ↓
Request / Response Handling
      ↓
Error Handling
      ↓
Authentication
      ↓
JWT
      ↓
Authorization
      ↓
RBAC

This keeps the project aligned with the concepts being studied.

Current Progress

Completed project concepts:

Task Manager REST API setup
Flask routing
CRUD operations
Request and response handling
Authentication and authorization architecture
JWT authentication
JWT access-token handling
Authorization
Role-Based Access Control

Current focus:

Applying authorization rules to task operations
Separating authentication from authorization
Enforcing role and permission checks
Future Improvements

Planned improvements include:

Database persistence
Better password hashing
Token refresh mechanism
More granular permissions
Automated tests
Logging
Dockerization
Production deployment
Improved configuration management
API documentation

The project will continue evolving as new backend, system-design, SQL, and Python concepts are introduced throughout the roadmap.
