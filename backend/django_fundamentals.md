# Django Fundamentals

## Day 21 Focus

Day 21 introduces Django at the framework level, with emphasis on the
relationship between a Django **project** and its **apps**.

---

## Project vs App

A Django project is the configuration and deployment container for a Django
application.

A Django app is a focused unit of functionality that can contain models,
views, URLs, tests, and other application code.

```text
Django Project
│
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py

Django App
│
├── models.py
├── views.py
├── urls.py
├── admin.py
└── tests.py
```

A single project can contain multiple apps.

---

## Typical Structure

```text
url_shortener/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── shortener/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

The names can vary. The important distinction is between project-level
configuration and app-level domain functionality.

---

## Request Flow

A simplified Django request flow is:

```text
HTTP Request
     ↓
Project URL Configuration
     ↓
App URL Configuration
     ↓
View
     ↓
Application Logic
     ↓
Model / Database
     ↓
HTTP Response
```

Django provides conventions around routing, models, forms, administration,
middleware, and other common web-application concerns.

---

## Core Files

### `settings.py`

Contains project configuration such as installed apps, middleware, database
configuration, and other framework settings.

### `urls.py`

Maps URL patterns to views or included app URL configurations.

### `models.py`

Defines database-backed application models.

### `views.py`

Contains request-handling logic.

### `admin.py`

Registers models and customizes their Django admin representation.

### `manage.py`

Provides the command-line entry point for common Django project operations.

---

## App Boundaries

For the URL Shortener project, the initial app can be focused on short-link
creation and resolution:

```text
URL Shortener
      │
      └── shortener app
          ├── models
          ├── views
          ├── urls
          └── tests
```

Keep the app focused on the domain rather than creating one large app for
unrelated functionality.

---

## Day 21 Takeaways

- A project is the application container and configuration boundary.
- An app is a focused unit of domain functionality.
- URL routing connects incoming requests to views.
- Models represent database-backed application data.
- The project/app distinction is foundational for organizing a larger Django
  backend.

---

## Day 22 — Models, Migrations & Admin

Day 22 builds on the project/app fundamentals from Day 21 by introducing
Django's database-backed model layer.

### Models

Models define application data as Python classes.

```python
class ShortURL(models.Model):
    short_code = models.CharField(max_length=32, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

### Migrations

Migrations are version-controlled schema changes derived from model definitions.

Typical workflow:

```text
models.py
   |
   v
makemigrations
   |
   v
migration file
   |
   v
migrate
   |
   v
database schema
```

### Django Admin

Models can be registered with Django Admin to provide a basic administrative
interface for viewing and managing application data.

The URL Shortener project demonstrates this with:

- `models.py`
- `admin.py`
- `migrations/0001_initial.py`

### Day 22 Takeaways

- Models represent database-backed domain entities.
- Migrations track schema changes over time.
- Admin provides a convenient interface for model data.
- Model design should reflect clear domain boundaries.

---
