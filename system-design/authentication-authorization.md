# Authentication & Authorization

Authentication and authorization are separate responsibilities in a backend system.

- **Authentication** determines who the user is.
- **Authorization** determines what the authenticated user is allowed to do.

---

## Basic Architecture

A typical request flow can look like:

```text
Client
  |
  v
Load Balancer / Reverse Proxy
  |
  v
Backend API
  |
  +----> Authentication
  |
  +----> Authorization
  |
  v
Application Services
  |
  v
Database
```

Authentication should happen before protected application resources are accessed.

Authorization should then determine whether the authenticated user has permission to perform the requested operation.

---

## Authentication Flow

A simplified login flow:

1. Client sends credentials
        |
        v
2. API validates the request
        |
        v
3. Server verifies password hash
        |
        v
4. Server establishes authenticated identity
        |
        v
5. Client receives authentication credential

The server should never store plaintext passwords.

Passwords should be stored using a strong password-hashing algorithm with an appropriate configuration.

---

## Authorization

After authentication, the application can determine what the user is allowed to access.

For example:

User
 |
 +-- role: user
 |      |
 |      +-- read own tasks
 |      +-- create own tasks
 |      +-- update own tasks
 |
 +-- role: admin
        |
        +-- read all tasks
        +-- manage users
        +-- administrative operations

Authorization checks should be performed on protected resources rather than relying only on the client to enforce permissions.

---

## Session-Based Authentication

With session-based authentication:

Client
  |
  | Login
  v
Backend
  |
  | Create session
  v
Session Store
  |
  | Session ID
  v
Client

The client sends the session identifier with subsequent requests.

The server uses the session identifier to retrieve the authenticated user's session.

---

## Token-Based Authentication

With token-based authentication:

Client
  |
  | Login
  v
Authentication Service
  |
  | Access Token
  v
Client
  |
  | Authorization: Bearer <token>
  v
Backend API

The API validates the token before processing protected requests.

JWT is one example of a token format, but token-based authentication does not necessarily require JWT.

---

## Security Considerations

A production authentication system should consider:

- HTTPS
- Password hashing
- Secure credential storage
- Token/session expiration
- Token rotation where appropriate
- Secure cookies
- CSRF protection where applicable
- Rate limiting
- Account lockout or abuse protection
- Authorization checks
- Input validation
- Secret management
- Audit logging
- Least-privilege access

---

## Authentication vs Authorization

| Authentication         | Authorization                         |
| ---------------------- | ------------------------------------- |
| Identifies the user    | Determines permissions                |
| Happens first          | Happens after identity is established |
| Example: login         | Example: access control               |
| Answers "Who are you?" | Answers "What can you do?"            |

---

## Backend Example

For the Task Manager API:

POST /login
     |
     v
Authenticate user
     |
     v
Create authenticated session/token
     |
     v
GET /tasks
     |
     v
Authenticate request
     |
     v
Authorize access to tasks
     |
     v
Return permitted resources

The API should verify that a user is allowed to access the requested task instead of trusting a user-provided identifier alone.

---

## Design Principles

A scalable authentication architecture should:

1. Keep authentication separate from business logic.
2. Centralize authentication mechanisms where appropriate.
3. Keep authorization close to resource access decisions.
4. Avoid storing plaintext passwords.
5. Use secure transport.
6. Follow least-privilege principles.
7. Make authentication failures observable through appropriate logging and monitoring.
8. Keep secrets outside source control.
