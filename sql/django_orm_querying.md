# Django ORM Querying

Day 23 focuses on writing efficient Django ORM queries when related models
are involved.

The main topics are:

- Related-object querying
- `select_related()`
- `prefetch_related()`
- Foreign-key and one-to-one relationships
- Many-to-many and reverse relationships
- Avoiding repeated database queries
- Choosing eager-loading strategies deliberately

---

## Related Objects

Suppose a URL Shortener application later adds an owner relationship:

```python
class ShortURL(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    short_code = models.CharField(max_length=32, unique=True)
```

Accessing `url.owner` may require another database query when the related
object has not already been loaded.

---

## `select_related()`

`select_related()` is designed for single-valued relationships such as
`ForeignKey` and `OneToOneField`.

```python
urls = ShortURL.objects.select_related("owner").all()

for url in urls:
    print(url.short_code, url.owner.username)
```

Django can load the related object using SQL joins rather than issuing a
separate query for every row.

Use it when the relationship can be represented as a single related object.

---

## `prefetch_related()`

`prefetch_related()` is designed for collections such as many-to-many and
reverse foreign-key relationships.

```python
users = User.objects.prefetch_related("short_urls").all()

for user in users:
    for url in user.short_urls.all():
        print(user.username, url.short_code)
```

Django performs separate queries and combines the results in Python.

Use it when the relationship returns multiple related objects.

---

## `select_related()` vs `prefetch_related()`

| Technique | Best for | Typical strategy |
|---|---|---|
| `select_related()` | ForeignKey / OneToOne | SQL join |
| `prefetch_related()` | ManyToMany / reverse FK | Separate query + Python join |

The goal is not to load everything eagerly. The goal is to load the related
data that the request actually needs without creating repeated queries.

---

## N+1 Query Pattern

A common inefficient pattern is:

```python
urls = ShortURL.objects.all()

for url in urls:
    print(url.owner.username)
```

If each `owner` access triggers another query, one query for the URL list can
turn into many additional queries.

A related-object strategy can reduce this pattern:

```python
urls = ShortURL.objects.select_related("owner")
```

---

## Query Composition

Filtering and eager loading can be combined:

```python
urls = (
    ShortURL.objects
    .filter(is_active=True)
    .select_related("owner")
    .order_by("-created_at")
)
```

Keep query construction readable and select only the relationships required
by the response or business operation.

---

## Practical Checklist

- Identify which related objects the endpoint actually uses.
- Use `select_related()` for single-valued relationships.
- Use `prefetch_related()` for collections.
- Watch for N+1 query patterns.
- Inspect generated SQL when query behavior is unclear.
- Avoid eager loading relationships that the request does not need.
- Measure query count when optimizing an API endpoint.

---

## Interview Checklist

- What problem does `select_related()` solve?
- When should `prefetch_related()` be used instead?
- What is the N+1 query problem?
- How does `select_related()` differ from a Python-side join?
- Why can eager loading itself become wasteful?
