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
- Django
- Django REST Framework
- FastAPI
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
- Structured logging configuration
- Basic automated testing

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
```text
├── app.py
├── flask_basics.py
├── flask_routing.py
├── authentication.py
├── authorization.py ← NEW
├── error_handling.py
├── jwt_authentication.py
└── request_response.py
```

The long-term direction is:

```text
Client
   ↓
```
Flask Application
```text
   ↓
```
Routes / Blueprints
```text
   ↓
Service Layer
   ↓
Database / Models

```
The service and database layers will be introduced as the project progresses through the roadmap.

---

Current authentication/authorization concepts:

- JWT authentication
- Authorization
- Role-Based Access Control
- Permissions
- Resource ownership

---

## Testing

Day 15 introduces comprehensive testing for the Task Manager API.

Testing implementation includes:

- pytest-flask integration
- Fixtures for Flask applications
- Test client for simulating HTTP requests
- Authentication and authorization tests
- Task operation tests
- Permission and access control tests
- Test configuration with `conftest.py`

Test files:

- `tests/conftest.py` — Pytest fixtures and configuration
- `tests/test_tasks.py` — Task CRUD operations and filtering tests
- `tests/test_auth.py` — Authentication, authorization, and token tests

The tests serve as both verification and documentation of API behavior.

---

### Day 18

The Task Manager now includes:

- Standardized API error responses
- Error codes
- Consistent HTTP status handling
- Generator-based task processing
- Lazy task pipelines
- Generator-based filtering

---

## Day 22 — URL Shortener Django Model

The URL Shortener project now moves from requirements/schema work into
Django-backed domain modeling.

Added:

- `projects/url-shortener/models.py`
- `projects/url-shortener/admin.py`
- `projects/url-shortener/migrations/0001_initial.py`

The `ShortURL` model contains:

- `short_code`
- `original_url`
- `created_at`
- `expires_at`
- `is_active`

The initial migration captures the database schema represented by the Django
model, while the admin registration provides a basic administrative interface
for inspecting and managing short URLs.

---

## Day 23 — URL Shortener DRF API

The URL Shortener now moves from Django persistence into its first API layer.

Added:

- `projects/url-shortener/serializers.py`
- `projects/url-shortener/views.py`
- `projects/url-shortener/urls.py`

The DRF layer provides list/create and detail endpoints for active short URLs.
Serializers define the API representation while generic DRF views handle the
request/response flow.

---

## Planned Enhancements

- SQLite Integration
- SQLAlchemy
- Service Layer
- Request Validation
- Testing
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

---

## Day 24 — URL Shortener Validation + API Responses

The URL Shortener now adds a stronger API boundary around the DRF layer.

Added or updated:

- Serializer validation for URLs and expiration timestamps
- Server-generated unique short codes
- DRF ViewSet structure
- Router-based URL registration
- Permission classes
- Consistent success response envelopes

The implementation remains limited to the roadmap's current list/create/detail
API scope rather than pulling future authentication and administration work
forward.

## Day 25 — URL Shortener Authentication & Admin

The URL Shortener now introduces authenticated ownership.

Added or updated:

- `projects/url-shortener/permissions.py`
- `projects/url-shortener/migrations/0002_shorturl_owner.py`
- Owner field on `ShortURL`
- Authenticated DRF access
- Owner-scoped URL listing and retrieval
- Django admin ownership visibility

New short URLs are associated with the authenticated Django user.

---

## Day 26 — URL Shortener FastAPI Comparison

Day 26 adds a small FastAPI implementation of the URL Shortener alongside the
existing Django/DRF version. The goal is framework comparison, not replacement
of the existing project implementation.

Added:

- `projects/url-shortener/fastapi_app.py`

The comparison implementation demonstrates:

- FastAPI application and route declarations
- Request validation with Pydantic models
- Response models
- Dependency injection
- Create, list, and retrieve URL endpoints
- Explicit HTTP error responses

The FastAPI version uses an in-memory store intentionally. The existing Django
model, migrations, authentication, ownership, and DRF implementation remain the
source of truth for the project's persistent implementation at this stage.

---

## Day 27 — URL Shortener FastAPI Validation & Dependency Injection

Day 27 extends the FastAPI comparison implementation with stronger request and
response contracts and reusable dependencies.

Updated:

- `projects/url-shortener/fastapi_app.py`

The implementation demonstrates:

- Pydantic request validation
- Response models
- Header-based request context
- Dependency injection with `Depends`
- Injected storage access
- Explicit HTTP error responses

The Django/DRF implementation remains the persistent project source of truth;
the FastAPI implementation continues to serve as a framework comparison and
learning artifact.

---

## Day 28 — URL Shortener Async Endpoint

The URL Shortener FastAPI comparison now includes an asynchronous endpoint.

Updated:

- `projects/url-shortener/fastapi_app.py`

The FastAPI list endpoint is now declared with `async def` and yields to the
event loop before returning the in-memory collection. This keeps the project
aligned with the day's async FastAPI focus without replacing the existing
Django/DRF implementation.

---

## Day 29 — URL Shortener Complete Test Suite

Day 29 completes the FastAPI comparison testing layer for the URL Shortener.

Added:

- `projects/url-shortener/tests/conftest.py`
- `projects/url-shortener/tests/test_fastapi_app.py`
- `projects/url-shortener/tests/__init__.py`

The test suite covers:

- FastAPI `TestClient`
- Dependency overrides
- Isolated in-memory stores
- Successful URL creation
- Request validation
- URL listing
- URL retrieval
- `404 Not Found` behavior

The existing Django/DRF implementation and all earlier project work remain
unchanged.

---

## Day 30 — URL Shortener Milestone + README

Day 30 consolidates the URL Shortener work completed during Days 21–29.

Milestone review:

- Django/DRF project structure
- URL model and migrations
- Serializer validation and API responses
- ViewSets, routers, and permissions
- Authentication and ownership
- FastAPI comparison implementation
- Async FastAPI endpoint
- API testing with dependency overrides
- Backward-compatible migration practices

The project README is updated as the phase checkpoint. No new application
feature is introduced on Day 30; the milestone focuses on consolidation,
documentation, and readiness for the database/distributed-systems phase.

---

## Day 31 — Expense Tracker Requirements

Day 31 starts the Expense Tracker project for the Databases & Distributed
Systems phase.

Added:

- `projects/expense-tracker/README.md`

The requirements define:

- Expense creation
- Expense listing and filtering
- Date-range queries
- Pagination
- Expense retrieval, update, and deletion
- Relational data requirements
- Validation and HTTP expectations
- Transaction and connection-pooling considerations

Day 31 intentionally defines the project boundary without implementing the
database schema or CRUD layer. Those implementation steps are scheduled for
Day 32.

---

## Day 32 — Expense Tracker Schema + CRUD

Day 32 moves the Expense Tracker from requirements into its first database
implementation layer.

Added:

- `projects/expense-tracker/schema.sql`
- `projects/expense-tracker/crud.py`

The implementation includes:

- Relational `expenses` table
- Positive monetary amount constraint
- Category and date indexes
- Create, retrieve, list, update, and delete operations
- Category and date-range filtering
- Stable pagination ordering
- SQLAlchemy 2.x `Session` usage
- Explicit transaction ownership at the service boundary

Day 32 builds on the requirements defined on Day 31 without replacing earlier
project work.

---

## Day 33 — Expense Tracker Background Aggregation

Day 33 extends the Expense Tracker with an aggregation workload suitable for
background processing.

Added:

- `projects/expense-tracker/background_aggregation.py`

The aggregation layer includes:

- Date-range filtering
- Grouping expenses by category
- Summing monetary amounts with SQL aggregation
- Stable category ordering
- A session-injected design suitable for a background worker

The aggregation is kept separate from the HTTP request path so it can later be
submitted to the worker-queue architecture introduced on Day 33.

---

## Day 34 — Expense Tracker Async Processing

Day 34 extends the Expense Tracker with an asynchronous producer/consumer
boundary for aggregation work.

Added:

- `projects/expense-tracker/async_processing.py`

The processing layer demonstrates:

- Async job submission
- `asyncio.Queue` coordination
- Background consumer tasks
- Queue completion tracking
- Running blocking handlers outside the event loop

The project continues to separate HTTP request handling from slower background
work without replacing the existing CRUD and aggregation layers.

---

## Day 35 — Expense Tracker Caching Layer

Day 35 extends the Expense Tracker with an application-level cache boundary
for expense lookups.

Added:

- `projects/expense-tracker/caching_layer.py`

The caching layer includes:

- Cache-aside lookup
- Repository/cache separation through protocols
- Stable cache-key generation
- Cache population on misses
- Explicit invalidation after writes
- An injectable design that can later use Redis

The cache is kept separate from the existing CRUD and asynchronous processing
layers so caching can evolve independently of the database access code.

---

## Day 36 — Expense Tracker Redis Caching

Day 36 extends the Expense Tracker caching layer with Redis-backed shared
caching.

Added:

- `projects/expense-tracker/redis_caching.py`

The implementation includes:

- Redis-backed expense caching
- JSON serialization
- TTL configuration
- Cache-aside reads
- Explicit invalidation
- Shared cache behavior across application instances
- A repository boundary that keeps Redis concerns isolated

The existing CRUD, aggregation, asynchronous processing, and application-level
caching layers remain intact.

---

## Day 37 — Expense Tracker Observability

Day 37 adds a lightweight observability layer to the Expense Tracker.

Added:

- `projects/expense-tracker/observability.py`

The observability layer includes:

- Correlation IDs
- Structured JSON request events
- Request duration measurement
- HTTP method/path/status metadata
- Bounded log fields

The existing CRUD, aggregation, asynchronous processing, application caching,
Redis caching, and reliability layers remain intact.

---

## Day 38 — Expense Tracker Reliability

Day 38 adds a bounded reliability layer to the Expense Tracker.

Added:

- `projects/expense-tracker/reliability.py`

The reliability layer includes:

- Transient dependency errors
- Bounded retry attempts
- Exponential backoff
- Jitter
- Injectable sleep and randomness for deterministic testing

The existing CRUD, aggregation, asynchronous processing, caching, Redis
caching, and observability layers remain intact.

---

## Day 39 — Expense Tracker Architecture Refactor

Day 39 refactors the Expense Tracker around explicit application boundaries.

Added:

- `projects/expense-tracker/architecture_refactor.py`

The refactor includes:

- Domain entity separation
- Service-layer application rules
- Repository protocol
- Dependency injection
- Storage adapter isolation
- Transport-independent validation

The existing CRUD, aggregation, asynchronous processing, caching, Redis
caching, observability, and reliability layers remain intact.

---

## Day 40 — Expense Tracker Milestone

Day 40 consolidates the Expense Tracker work completed during the Databases &
Distributed Systems phase.

Milestone review:

- CRUD and domain validation
- Aggregation and asynchronous processing
- Database design and concurrency handling
- Application caching and Redis caching
- Structured logging and observability
- Retry and reliability patterns
- Service and repository boundaries
- Clean architecture and dependency injection
- Circuit-breaker and bulkhead considerations

No new feature is introduced on Day 40. The milestone confirms that the
Expense Tracker reflects the distributed-systems and backend-engineering
patterns covered through Day 39 while preserving all earlier functionality.

---

## Day 41 — Task Manager Dockerization

Day 41 moves the Task Manager toward a containerized runtime.

Added:

- `projects/task-manager/Dockerfile`
- Root `.dockerignore`

The Dockerization:

- Uses a Python slim base image
- Installs the repository's Python dependencies
- Copies the existing backend and Task Manager project code
- Exposes port `5000`
- Starts the Flask application on `0.0.0.0`

No application logic is replaced. Docker Compose and the multi-container
application stack are introduced on Day 42.

---

## Day 42 — Expense Tracker Container Stack

Day 42 extends the repository's containerization work into a local
multi-service stack.

Added:

- `docker-compose.yml`
- `sql/container_migrations.sql`
- `system-design/local-distributed-environment.md`
- `dsa/dynamic_programming/word_break.py`
- `dsa/dynamic_programming/coin_change_ii.py`

The Compose stack provides:

- Flask application container
- PostgreSQL database container
- Redis cache container
- Persistent PostgreSQL volume
- Database health checks
- Redis health checks
- Containerized initialization and migration scripts

The existing application and Expense Tracker database layers remain intact.
The stack establishes the local infrastructure boundary needed for later
production-engineering work.

---

## Day 43 — Repository CI Checks

Day 43 adds the repository's first continuous-integration workflow.

Added:

- `.github/workflows/ci.yml`
- `backend/ci-basics.md`
- `system-design/cicd-pipeline.md`
- Python environment/configuration example
- Production migration example
- Sliding-window and two-pointer review problems

The CI workflow validates Python linting, automated tests, and Docker image
construction on pushes and pull requests.

---

## Day 44 — CI Pipeline & Test Coverage

Day 44 extends repository CI from basic validation toward a production-ready
quality gate.

Added:

- Automated test coverage reporting with `pytest-cov`
- Coverage execution in GitHub Actions
- CI documentation for the test/coverage stage
- Clear separation between validation and future deployment stages

The CI pipeline now validates linting, tests, coverage, and Docker image
construction before a change is considered ready for delivery.

---

## Day 45 — Deployment-ready Task Manager

Day 45 prepares the Task Manager for production-style serving.

Added/updated:

- Environment-driven application configuration
- WSGI entry point
- Gunicorn production server
- Deployment-oriented Docker startup command
- Runtime configuration documentation

The Task Manager can now be served by Gunicorn inside the existing Docker image,
with a reverse proxy positioned in front of the application server in a
production architecture.

---

## Day 46 — Task Manager Health Checks + Structured Logs

Day 46 adds production monitoring hooks to the Task Manager project.

Added:

- `projects/task-manager/health_checks.py`
- `projects/task-manager/structured_logging.py`
- `projects/task-manager/tests/test_health_checks.py`
- Flask registration of `/health/live` and `/health/ready` through
  `backend/monitoring_health_checks.py`

The project now distinguishes process liveness from dependency-aware
readiness and emits structured JSON log records suitable for centralized
collection.

---

## Day 47 — Task Manager Security Hardening

Day 47 applies a security hardening pass to the Task Manager project.

Added:

- `projects/task-manager/security_hardening.py`
- `projects/task-manager/tests/test_security_hardening.py`

The hardening pass covers:

- Explicit CORS allow-list handling
- CSRF requirements for cookie-authenticated state-changing requests
- CSRF token comparison
- Production secret validation
- Baseline browser security headers

The implementation keeps secrets outside source control and avoids logging
security-sensitive token values.

---

## Day 49 — Expense Tracker Failure Simulation

Day 49 adds controlled incident simulation to the Expense Tracker.

Added:

- `projects/expense-tracker/failure_simulation.py`
- Production failure and recovery runbook

The simulation exercises dependency failure, rollback decision recording,
recovery-mode transitions, restoration, and incident evidence without requiring
a real production outage.

---

## Day 50 — Expense Tracker Production Milestone

Day 50 is the Production Engineering milestone for the Expense Tracker.

Milestone review:

- Deployment and configuration readiness
- Health checks and observability
- Security hardening and dependency controls
- Database reliability and troubleshooting
- Failure simulation and recovery
- Incident handling and rollback decisions
- Testing and operational error handling
- Documentation of the production-readiness state

No new application feature is required on Day 50. The milestone verifies that
the Expense Tracker documents the production-engineering practices developed
during Days 41–49 while preserving all earlier functionality.

---

## Day 60 — RAG/Agent Prototype

Day 60 closes the GenAI Engineering phase with a small provider-neutral
RAG/Agent prototype.

Added:

- `projects/rag-agent-prototype/rag_agent.py`
- `projects/rag-agent-prototype/README.md`

The prototype demonstrates:

- Document ingestion into normalized chunks
- Simple lexical retrieval with explicit top-k selection
- Context assembly for an answer step
- An application-owned tool registry
- Tool argument validation before execution
- A small agent loop that decides between retrieval and an approved tool
- Clear boundaries between retrieval, tools, orchestration, and answer generation

The implementation is intentionally deterministic and provider-neutral. It is a
learning prototype, not a production replacement for a managed model or vector
database.

---

## Day 61 — Task Manager LLD Data Structures Review

Day 61 starts the System Design & LLD phase by reviewing the Task Manager's
domain data structures and their service boundaries.

Added:

- `projects/task-manager/lld_data_structures.py`

The review artifact demonstrates:

- Task status as an explicit domain type
- Task dependency relationships
- Repository-style storage abstraction
- In-memory implementation for deterministic review
- A service layer that enforces dependency completion before a task can be
  completed
- Composition through dependency injection rather than framework coupling

This is an LLD review increment; it does not replace the existing Task Manager
API, authentication, security, or production-oriented components.

---

## Day 62 — Expense Tracker LLD

Day 62 applies Factory and Strategy patterns to the existing Expense Tracker
project without replacing its production-oriented layers.

Added:

- `projects/expense-tracker/lld_design.py`

The LLD artifact demonstrates:

- Expense as a small domain entity
- Strategy contract for interchangeable report behavior
- Factory for explicit report-strategy creation
- Application-service coordination through abstractions
- Reuse of the existing Expense Tracker domain rather than a separate sample
  application

The artifact is intentionally separate from the existing CRUD, caching,
observability, reliability, and production-engineering implementations.

---

## Day 63 — Notification Service LLD

Day 63 adds a focused LLD artifact for a notification service.

Added:

- `projects/notification-service/lld_design.py`
- `projects/notification-service/README.md`

The artifact demonstrates:

- Observer-based notification fan-out
- Adapter-based integration with an external email provider
- Small protocol-oriented contracts
- Composition of application and infrastructure boundaries
- Validation at the application service boundary
- Production considerations for retries, idempotency, queues, and delivery state

The artifact is intentionally separate from the existing Task Manager and
Expense Tracker projects so the new LLD milestone does not replace earlier
project layers.

---

## Day 65 — URL Shortener Design Document

Day 65 turns the URL Shortener HLD into a reusable design document for
architecture review and interview discussion.

Added:

- `projects/url-shortener/design_document.md`

The document records:

- Functional and non-functional requirements
- Versioned API contracts
- URL/User service ownership
- Data model and constraints
- Redirect and create flows
- Scaling and caching strategy
- Reliability and observability
- API evolution and deprecation strategy
- Interview explanation sequence

The design document complements the existing Day 64 `hld_design.md` and does
not replace earlier project implementations.

---

## Day 66 — Rate Limiter Design

Day 66 adds the Rate Limiter as the next scalable-service design milestone.

Added:

- `projects/rate-limiter/README.md`
- `projects/rate-limiter/design_pseudocode.md`

The artifact demonstrates:

- Token-bucket enforcement
- Deterministic rate-limit keys
- Atomic shared-state updates
- HTTP 429 and retry behavior
- Explicit fail-open/fail-closed policy choices
- Capacity and observability considerations
- Interview-ready explanation flow

The project is intentionally design-first and complements the standalone Rate
Limiter HLD in `system-design/rate-limiter-hld.md`.

---

## Day 67 — Notification System Design

Day 67 turns the existing Notification Service LLD into a portfolio-ready
high-level system design.

Added:

- `projects/notification-service/notification_system_design.md`

The design documents:

- API contracts
- Notification and delivery state
- Transactional outbox flow
- Broker and channel-worker architecture
- At-least-once delivery and idempotency
- Retry and dead-letter handling
- Capacity, reliability, and security boundaries

The new design complements the existing Observer/Adapter LLD rather than
replacing it.

---

## Day 68 — Chat Application Architecture

Day 68 adds a project-oriented architecture artifact for the Chat Application
milestone.

Added:

- `projects/chat-application/README.md`
- `projects/chat-application/architecture.md`

The artifact documents:

- WebSocket gateway responsibilities
- Chat API and durable persistence boundaries
- Cross-instance pub/sub or broker fan-out
- Message send and reconnect flows
- Idempotency and ordering
- Backpressure and slow-consumer handling
- Reliability and implementation boundaries

The project remains design-first and complements the standalone Chat Application
HLD in `system-design/chat-application-hld.md`.

---

## Day 69 — News Feed Architecture

Day 69 adds a project-oriented architecture artifact for the News Feed milestone.

Added:

- `projects/news-feed/README.md`
- `projects/news-feed/architecture.md`

The artifact documents:

- Personalized feed read and post-publication flows
- Hybrid fan-out policy
- Cursor pagination
- Bounded caching
- Asynchronous feed propagation
- Eventual consistency and freshness
- Reliability and observability boundaries

The project remains design-first and complements the standalone News Feed HLD in
`system-design/news-feed-hld.md`.
