# Django ORM Basics

Day 22 introduces the Django ORM as the application-facing layer for
working with relational database data.

The focus is on:

- Django models
- Model fields
- QuerySets
- Creating records
- Reading records
- Updating records
- Deleting records
- Filtering
- Ordering
- QuerySet laziness
- Avoiding unnecessary database queries

---

## Model

A Django model is a Python class that represents a database-backed entity.

Example:

```python
from django.db import models


class ShortURL(models.Model):
    short_code = models.CharField(max_length=32, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

Django uses the model definition to generate database schema through
migrations.

---

## QuerySets

A QuerySet represents a collection of database records.

```python
active_urls = ShortURL.objects.filter(is_active=True)
```

Common operations include:

```python
ShortURL.objects.all()
ShortURL.objects.filter(is_active=True)
ShortURL.objects.get(short_code="abc123")
ShortURL.objects.order_by("-created_at")
ShortURL.objects.count()
```

---

## Creating Records

```python
short_url = ShortURL.objects.create(
    short_code="abc123",
    original_url="https://example.com",
)
```

The ORM translates this operation into an SQL `INSERT`.

---

## Updating Records

```python
short_url.is_active = False
short_url.save(update_fields=["is_active"])
```

For bulk updates:

```python
ShortURL.objects.filter(is_active=True).update(is_active=False)
```

---

## Deleting Records

```python
short_url.delete()
```

Bulk deletion:

```python
ShortURL.objects.filter(is_active=False).delete()
```

---

## Filtering

Multiple conditions can be expressed through keyword arguments:

```python
ShortURL.objects.filter(
    is_active=True,
    original_url__contains="example",
)
```

Common lookup expressions include:

- `exact`
- `contains`
- `icontains`
- `in`
- `gt`
- `gte`
- `lt`
- `lte`
- `isnull`

---

## QuerySet Laziness

Many QuerySet operations build a query without immediately executing it.

```python
queryset = ShortURL.objects.filter(is_active=True)
```

The database query is generally executed when the results are needed,
for example when iterating over the QuerySet or converting it to a list.

This allows Django to compose queries before execution.

---

## ORM vs SQL

The ORM improves developer productivity and keeps database access close to
the application's domain model.

Raw SQL can still be appropriate for:

- Database-specific features
- Highly specialized queries
- Complex reporting workloads
- Cases where the generated SQL needs precise control

The choice should be based on readability, correctness, performance,
maintainability, and the capabilities required by the query.

---

## Interview Checklist

- What is a Django model?
- What is a QuerySet?
- Why are QuerySets lazy?
- When does a QuerySet execute SQL?
- How do `filter()` and `get()` differ?
- How are records created and updated?
- When would raw SQL be preferable to ORM code?
- How do migrations connect models to database schema changes?
