# Django & Relational Database Indexing

Day 26 connects relational-database indexes with the way Django models declare
and use them.

## Why Indexes Matter

An index provides an additional data structure that can help the database find
matching rows without scanning the entire table. Indexes can improve reads, but
they also consume storage and add work to inserts, updates, and deletes.

## Django Field Indexes

For a simple single-column index, Django can declare `db_index=True`:

```python
class ShortURL(models.Model):
    short_code = models.CharField(max_length=32, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

A `unique=True` field already requires uniqueness enforcement through the
database, so adding another redundant index should be avoided unless there is a
specific reason.

## Django `Meta.indexes`

Use `Meta.indexes` for explicit, multi-column, conditional, or named indexes:

```python
class ShortURL(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
        ]
```

The column order matters. An index on `(owner, created_at)` is primarily useful
when queries constrain `owner` and then use `created_at` for filtering or
ordering.

## Composite Indexes

Relational databases can use composite indexes for common multi-column access
patterns:

```sql
CREATE INDEX idx_shorturl_owner_created
ON short_url(owner_id, created_at DESC);
```

The index should reflect real query patterns rather than every column that might
be filtered someday.

## Query Planning

Use the database's query planner to verify whether an index is useful. In
PostgreSQL, `EXPLAIN` and `EXPLAIN ANALYZE` are common tools:

```sql
EXPLAIN ANALYZE
SELECT *
FROM short_url
WHERE owner_id = 10
ORDER BY created_at DESC;
```

Django's `QuerySet.explain()` can expose the database execution plan:

```python
ShortURL.objects.filter(owner=user).order_by("-created_at").explain()
```

## Index Trade-Offs

| Benefit | Cost |
|---|---|
| Faster selective reads | Extra storage |
| Faster filtering and ordering for matching patterns | Slower writes |
| Can reduce full-table scans | More indexes to maintain |

## Common Mistakes

- Indexing every column without measuring query patterns.
- Creating duplicate indexes that enforce no additional requirement.
- Ignoring column order in composite indexes.
- Assuming an index guarantees a faster query regardless of selectivity.
- Forgetting that indexes must be maintained during writes.

## Day 26 Takeaways

- Django can create indexes through `db_index` and `Meta.indexes`.
- Composite indexes should match real filtering and ordering patterns.
- `EXPLAIN` and `QuerySet.explain()` help verify index usage.
- Indexes are a read-performance trade-off, not a universal optimization.
