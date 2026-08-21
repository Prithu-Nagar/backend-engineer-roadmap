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
