# API Gateway

An API Gateway is a centralized entry point through which clients communicate with backend services.

Instead of clients communicating directly with multiple services, requests can be routed through a single gateway.

Client
   |
   v
API Gateway
   |
   +----> User Service
   |
   +----> Task Service
   |
   +----> Order Service

---

## Why Use an API Gateway?

An API Gateway can centralize common API-level responsibilities such as:

- Request routing
- Authentication
- Rate limiting
- Request validation
- Logging
- Monitoring
- API versioning
- Request and response transformation

---

## Request Routing

The gateway determines which backend service should handle a request.

Example:

GET /users
    |
    v
API Gateway
    |
    v
User Service

GET /tasks
    |
    v
API Gateway
    |
    v
Task Service

The client does not need to know the internal service topology.

---

## Authentication

The API Gateway can validate an access token before forwarding a request.

Client
    |
    | Authorization: Bearer <token>
    v
API Gateway
    |
    | Token validation
    v
Backend Service

Authentication identifies the requester.

Authorization determines whether that requester is allowed to perform a particular action.

Resource-level authorization should still be enforced by the service that owns the resource.

---

## Rate Limiting

An API Gateway can limit how frequently clients can make requests.

Example:

100 requests per minute per user

If the limit is exceeded:

Client
    |
    v
API Gateway
    |
    v
429 Too Many Requests

Rate limiting protects backend services from excessive traffic.

---

## TLS Termination

The API Gateway can terminate external HTTPS connections.

Client
    |
    | HTTPS
    v
API Gateway
    |
    v
Backend Services

This can centralize certificate management.

---

## Request Transformation

The gateway can modify or validate a request before forwarding it.

Client Request
    |
    v
API Gateway
    |
    v
Transformed Request
    |
    v
Backend Service

Transformation should be kept limited so that the gateway does not become a business-logic layer.

---

## API Aggregation

A client may need information from multiple services.

Without aggregation:

Client
    |
    +----> User Service
    |
    +----> Task Service
    |
    +----> Notification Service

With gateway aggregation:

Client
    |
    v
API Gateway
    |
    +----> User Service
    |
    +----> Task Service
    |
    +----> Notification Service
    |
    v
Combined Response
    |
    v
Client

This can reduce the number of network requests made by clients.

---

## API Gateway vs Reverse Proxy

A reverse proxy forwards requests to backend servers.

An API Gateway can provide reverse-proxy functionality while also handling API-specific concerns such as:

- Authentication
- Rate limiting
- API routing
- API versioning
- Request transformation
- Observability

Therefore, an API Gateway is generally more API-aware than a basic reverse proxy.

---

## API Gateway vs Load Balancer

A load balancer primarily distributes traffic across backend instances.

Example:

Client
    |
    v
Load Balancer
    |
    +----> Server 1
    |
    +----> Server 2
    |
    +----> Server 3

An API Gateway focuses on API-level concerns.

They can also be used together:

Client
    |
    v
API Gateway
    |
    v
Load Balancer
    |
    +----> Service 1
    |
    +----> Service 2
    |
    +----> Service 3

---

## Authentication vs Authorization

Authentication answers:

"Who are you?"

Authorization answers:

"What are you allowed to do?"

Example:

Client
    |
    v
API Gateway
    |
    v
Authentication
    |
    v
Authenticated User
    |
    v
Task Service
    |
    v
Authorization
    |
    +----> Allowed
    |
    +----> Denied

The gateway can authenticate the user, while the backend service can enforce permissions for a specific resource.

---

## High Availability

The API Gateway can become a critical component of the architecture.

A single gateway instance can create a single point of failure.

A production architecture can use multiple gateway instances:

             Client
                |
                v
          Load Balancer
           /          \
          v            v
     Gateway 1    Gateway 2
          \            /
           \          /
            v        v
              Services

Health checks, monitoring, and automatic recovery should also be considered.

---

## Scaling

API Gateway instances can be horizontally scaled as traffic increases.

Example:

Load Balancer
    |
    +----> Gateway 1
    |
    +----> Gateway 2
    |
    +----> Gateway 3

The gateway should not become a throughput bottleneck.

---

## Observability

The API Gateway is a useful place for collecting API-level information such as:

- Request counts
- Response times
- Error rates
- Access logs
- Trace IDs

A request can carry a trace ID through the system:

Client
    |
    v
API Gateway
    |
    v
Trace ID
    |
    v
Backend Service
    |
    v
Database

This helps trace requests across multiple services.

---

## What Should Not Live in the Gateway?

The API Gateway should generally not contain application business logic.

Avoid:

API Gateway
    |
    +----> Business Rules
    |
    +----> Database Queries
    |
    +----> Order Processing
    |
    +----> User Management

Prefer:

API Gateway
    |
    +----> Routing
    |
    +----> Authentication
    |
    +----> Rate Limiting
    |
    +----> Observability
    |
    v
Backend Services
    |
    +----> Business Logic
    |
    +----> Data Access

---

## Common Interview Questions

### What is an API Gateway?

An API Gateway is a centralized entry point for API traffic that routes requests to backend services and can provide common API-level functionality.

### Is an API Gateway the same as a reverse proxy?

No.

An API Gateway can provide reverse-proxy functionality but generally provides additional API-specific capabilities.

### Is an API Gateway a load balancer?

No.

A load balancer primarily distributes traffic, while an API Gateway handles API-level concerns.

### Should all authorization happen at the gateway?

No.

The gateway can perform authentication and centralized policy checks, but resource-level authorization should generally be enforced by the service that owns the resource.

### Should business logic be placed in the gateway?

Generally no.

Business logic should remain inside the appropriate backend service.

### Can an API Gateway become a single point of failure?

Yes.

Multiple gateway instances, load balancing, health checks, monitoring, and automatic recovery can improve availability.

---

## Revision Summary

API Gateway:

Client
    |
    v
API Gateway
    |
    +----> Authentication
    |
    +----> Rate Limiting
    |
    +----> Routing
    |
    +----> Observability
    |
    v
Backend Services

Remember:

Reverse Proxy
→ Forwards traffic

Load Balancer
→ Distributes traffic

API Gateway
→ Central API entry point and API-level cross-cutting concerns
