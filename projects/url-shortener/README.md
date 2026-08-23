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
