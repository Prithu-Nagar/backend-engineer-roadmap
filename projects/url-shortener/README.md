# URL Shortener

Day 21 starts a new backend project: a production-oriented URL shortener.

## Goal

Accept a long URL, generate a unique short code, and redirect requests
from the short URL to the original destination.

## Core Requirements

### Create Short URL

The API should accept:

- Original URL
- Optional custom alias, if supported

The response should return:

- Short code
- Short URL
- Original URL

### Redirect

A request to:

```text
GET /<short_code>
```

should:

1. Look up the short code.
2. Verify that the record is active.
3. Redirect to the original URL.

### Validation

The service should validate:

- URL format
- Short-code uniqueness
- Required fields
- Reasonable URL length

### Persistence

The database should retain:

- Original URL
- Short code
- Creation timestamp
- Optional expiration timestamp
- Active/inactive state

The initial schema is provided in `schema.sql`.

## Suggested API Shape

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/urls` | Create a short URL |
| GET | `/<short_code>` | Redirect to the original URL |
| GET | `/api/urls/<short_code>` | Retrieve URL metadata |

## Example Request

```json
{
  "original_url": "https://example.com/articles/backend-engineering"
}
```

## Example Response

```json
{
  "short_code": "aB91x",
  "short_url": "https://short.example/aB91x",
  "original_url": "https://example.com/articles/backend-engineering"
}
```

## Initial Architecture

```text
Client
  |
  v
URL Shortener API
  |
  +----> URL Service
  |          |
  |          v
  |      Repository
  |          |
  |          v
  |       Database
  |
  +----> Redirect Handler
             |
             v
         URL Lookup
             |
             v
        HTTP Redirect
```

## Day 21 Scope

This day focuses on:

- Requirements
- Data model
- Database schema
- Clear API boundaries

Application implementation, framework integration, migrations, and
production concerns can be added in later project days.

---

## Day 22 — Django Model + Migration

Day 22 connects the existing URL Shortener requirements and relational schema
to Django's model layer.

### Model

File:

`models.py`

The `ShortURL` model contains:

| Field | Type | Purpose |
|---|---|---|
| `short_code` | `CharField` | Unique short identifier |
| `original_url` | `URLField` | Destination URL |
| `created_at` | `DateTimeField` | Creation timestamp |
| `expires_at` | `DateTimeField` | Optional expiration |
| `is_active` | `BooleanField` | Lifecycle state |

### Migration

File:

`migrations/0001_initial.py`

The initial migration creates the `ShortURL` table from the model definition.

### Django Admin

File:

`admin.py`

The model is registered with Django Admin with:

- List display for important fields
- Filtering by active state
- Search by short code and original URL

This establishes the first Django persistence layer for the URL Shortener
before API endpoints are added in later days.

---

## Day 23 — Django REST Framework Endpoints

Day 23 adds the first API layer to the Django-backed URL Shortener using
Django REST Framework.

### Serializer

File:

`serializers.py`

The `ShortURLSerializer` controls the API representation and validation of
`ShortURL` data.

### Endpoints

Files:

- `views.py`
- `urls.py`

The project now defines:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/urls/` | List active short URLs |
| POST | `/api/urls/` | Create a short URL |
| GET | `/api/urls/<short_code>/` | Retrieve active URL metadata |

The endpoint layer is intentionally small. Redirect handling remains a
separate concern from the API metadata endpoints.

### Day 23 Flow

```text
HTTP Request
     |
     v
DRF URL pattern
     |
     v
Generic API View
     |
     v
Serializer <----> ShortURL Model
     |
     v
HTTP Response
```

This keeps the API representation separate from the underlying Django model
while building on the persistence layer introduced on Day 22.

---

## Day 24 — Validation + API Responses

Day 24 strengthens the DRF API boundary introduced on Day 23.

### Validation

Files:

- `serializers.py`
- `validation.py`

The API now validates and normalizes the original URL, checks expiration
semantics, and generates a unique short code on creation rather than requiring
clients to supply one.

### ViewSet + Permissions

File:

`views.py`

The project uses a router-friendly `ShortURLViewSet` with explicit DRF
permission configuration. The current scope exposes list, create, and retrieve
operations.

### Router

File:

`urls.py`

A `DefaultRouter` registers the ViewSet and keeps endpoint URL generation
centralized.

### Response Shape

Successful responses use a small envelope:

```json
{
  "data": {
    "short_code": "aB91x"
  }
}
```

List responses also include lightweight metadata:

```json
{
  "data": [],
  "meta": {
    "count": 0
  }
}
```

This establishes a consistent response contract before later roadmap days add
authentication, administration, and broader API capabilities.


## Day 25 — Authentication + Admin

Day 25 adds authenticated ownership to the URL Shortener while preserving the
Day 24 validation and API response behavior.

### Ownership

The `ShortURL` model now has an optional Django user relationship so existing
records can migrate safely. New API-created records are assigned to the
authenticated user.

### Authentication

The DRF ViewSet now requires authentication. List and retrieve operations are
scoped to the current user's active URLs, preventing users from seeing another
user's resources.

### Permissions

File:

`permissions.py`

`IsShortURLOwner` provides an explicit object-level ownership check.

### Admin

The Django admin now exposes the owner in list, filter/search, and ownership
selection fields.

### Files

- `models.py`
- `serializers.py`
- `views.py`
- `urls.py`
- `admin.py`
- `permissions.py`
- `migrations/0002_shorturl_owner.py`

The Day 24 serializer validation, generated short codes, router, and consistent
`data`/`meta` response envelopes are retained.

---

## Day 26 — FastAPI Comparison Implementation

Day 26 adds a FastAPI version of the core URL Shortener API for framework
comparison while preserving the existing Django/DRF implementation.

### FastAPI Implementation

File:

`fastapi_app.py`

The example demonstrates:

- FastAPI route declarations
- Pydantic request and response models
- Dependency injection with `Depends`
- HTTP status codes and error responses
- Create, list, and retrieve operations

### Comparison

| Area | Django + DRF | FastAPI |
|---|---|---|
| Routing | Django URL configuration + DRF router | Decorator-based route declarations |
| Validation | DRF serializers | Pydantic models |
| Dependency handling | Django/DRF application patterns | FastAPI dependency injection |
| API schema | DRF/OpenAPI tooling | Automatic OpenAPI generation |
| Current project storage | Django ORM | In-memory comparison store |

The FastAPI implementation is deliberately small. It is a comparison artifact,
not a replacement for the authenticated Django/DRF URL Shortener.

---

## Day 27 — FastAPI Validation & Dependency Injection

Day 27 extends the FastAPI comparison implementation with explicit validation,
response contracts, and reusable dependencies.

### Validation

`CreateURLRequest` uses a Pydantic model to define the request contract. FastAPI
uses that model to validate the request body and expose the schema in generated
API documentation.

### Response Models

`ShortURLResponse` defines the fields returned by the API. Declaring
`response_model` keeps the response contract explicit and prevents accidental
exposure of unrelated internal values.

### Dependency Injection

The FastAPI implementation now injects:

- Request context from the `X-Request-Id` header.
- The URL store through a separate dependency.

This keeps endpoint functions focused on HTTP behavior while making supporting
components easier to replace in tests or future implementations.

The project still uses an in-memory FastAPI comparison store. The existing
Django/DRF models, migrations, authentication, ownership, and persistence remain
unchanged.

---

## Day 28 — Async FastAPI Endpoint

Day 28 extends the FastAPI comparison implementation with asynchronous request
handling.

### Async Endpoint

File:

`fastapi_app.py`

The URL listing endpoint now uses `async def` and yields to the event loop
before returning the in-memory collection.

This demonstrates the FastAPI async endpoint model while keeping the example
self-contained. In a real service, the awaited work would normally be an
async-compatible database or HTTP operation.

The existing Django/DRF implementation remains the persistent project source
of truth.

---

## Day 29 — Complete FastAPI Test Suite

Day 29 adds a complete API test suite for the FastAPI comparison
implementation.

### Test Fixtures

Files:

- `tests/conftest.py`
- `tests/__init__.py`

The test fixture overrides the URL-store dependency so each test receives an
isolated in-memory store.

### API Tests

File:

`tests/test_fastapi_app.py`

The suite covers:

- Successful URL creation
- Invalid URL validation
- Listing URLs
- Retrieving an existing short URL
- `404 Not Found` for missing URLs
- Dependency override behavior

The tests use FastAPI's `TestClient` so the endpoints are exercised through the
HTTP API boundary.

The existing Django/DRF implementation remains the persistent project source of
truth, while the FastAPI comparison implementation now has a repeatable test
suite.
