# Containerized Service Architecture

Day 41 introduces containerization as a deployment boundary for backend
services.

---

## What Containerization Provides

A container packages an application together with the runtime and dependencies
needed to execute it consistently.

For a Python backend, the image typically contains:

- Python runtime
- Application source code
- Python dependencies
- Runtime configuration defaults
- Startup command

The container should remain replaceable and should not be treated as the
permanent home of application state.

---

## Image vs Container

### Image

An image is an immutable template used to create containers.

It contains the application filesystem and the instructions needed to run it.

### Container

A container is a running instance of an image.

Multiple containers can be created from the same image.

```text
Dockerfile
    |
    v
  Image
    |
    +----------+
    |          |
    v          v
Container A  Container B
```

---

## Containerized Backend Architecture

A production-oriented service can be modeled as:

```text
Client
  |
  v
Load Balancer / Reverse Proxy
  |
  v
+---------------------------+
| Task Manager Containers   |
|                           |
|  Container 1              |
|  Container 2              |
|  Container 3              |
+---------------------------+
  |
  +-------------------+
  |                   |
  v                   v
Database            Cache
```

The application containers should be as stateless as practical so instances
can be replaced or scaled independently.

---

## Stateless Application Containers

A stateless container should avoid storing durable application state inside
its writable filesystem.

Durable state should normally live in dedicated systems such as:

- PostgreSQL
- Redis
- Object storage
- External queues

This allows a container to be stopped and replaced without losing important
application data.

---

## Dockerfile Responsibilities

A Dockerfile should make the runtime reproducible.

Typical stages are:

1. Select a suitable base image.
2. Set the working directory.
3. Copy dependency metadata.
4. Install dependencies.
5. Copy application code.
6. Expose the application port.
7. Define the startup command.

The order of dependency-related layers can also improve Docker build-cache
reuse.

---

## Resource Boundaries

Containerization does not automatically solve capacity problems.

Production design should still consider:

- CPU limits
- Memory limits
- Number of application instances
- Connection-pool size
- Request concurrency
- Startup time
- Container restart behavior
- Health and readiness strategy

---

## Failure Model

A container can fail because of:

- Application crashes
- Dependency failures
- Resource exhaustion
- Invalid configuration
- Host/node failures
- Image or deployment problems

The architecture should assume containers are replaceable.

A restart policy can improve recovery, but restarting a failed process is not a
substitute for diagnosing persistent dependency or application failures.

---

## Container vs Persistent State

Prefer this separation:

```text
Container
  |
  +-- Application code
  +-- Runtime
  +-- Dependencies

External systems
  |
  +-- Database state
  +-- Cache state
  +-- Durable messages
  +-- Uploaded files
```

Do not use a container's writable filesystem as the primary source of truth for
durable business data.

---

## Production Checklist

Before deploying a containerized backend, verify:

- The image has a minimal suitable base.
- Dependencies are installed reproducibly.
- The application binds to the expected interface and port.
- Secrets are not baked into the image.
- Logs are written to standard output/error where appropriate.
- Durable data is stored outside the application container.
- Resource requirements are understood.
- Shutdown and restart behavior are understood.
- The image can be rebuilt from the Dockerfile.

Day 41 focuses on the container boundary itself. Docker Compose,
CI/CD, deployment strategies, and production monitoring are intentionally
covered in later roadmap days.
