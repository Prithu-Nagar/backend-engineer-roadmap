# Pagination at Scale

Pagination limits the amount of data returned by an API request.

## Why Pagination Matters

Returning thousands or millions of records in one response can cause:

- High database load
- Large response payloads
- High memory usage
- Increased network latency
- Poor client performance

A paginated API limits the amount of data returned per request.

---

## OFFSET Pagination

Example:

```sql
SELECT *
FROM tasks
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 40;
```

### Advantages

- Simple to understand
- Easy to implement
- Supports direct page-number navigation

### Disadvantages

Large offsets can require the database to scan or skip many rows before returning the requested page.

Results can also shift when records are inserted or deleted between requests.

## Keyset / Cursor Pagination

Instead of saying:

> Give me page 50

the client says:

> Give me the next 20 records after this cursor.

Example:

```sql
SELECT id, title, created_at
FROM tasks
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

The cursor represents the last item from the previous page.

### Why a Unique Tie-Breaker Matters

If multiple rows have the same `created_at`, ordering only by `created_at` may produce unstable pagination.

Use a unique secondary field:

```sql
ORDER BY created_at DESC, id DESC
```

This creates a deterministic ordering.

## Filtering + Pagination

Filtering should be applied before pagination.

```text
Request
  ↓
Validate filters
  ↓
Filter records in database
  ↓
Apply stable ordering
  ↓
Apply pagination
  ↓
Return response
```

Do not fetch the entire dataset into application memory just to filter and paginate it when the database can perform those operations efficiently.

## Sorting

Never directly concatenate untrusted user input into SQL identifiers.

Instead, maintain an allow-list:

```python
ALLOWED_SORT_FIELDS = {
    "created_at",
    "priority",
    "id",
}
```

Then map accepted values to known SQL expressions.

## API Example

```http
GET /api/tasks?page=2&per_page=20&completed=false&sort_by=priority&sort_order=desc
```

A response can contain:

```json
{
  "tasks": [],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_previous": true
  }
}
```

## OFFSET vs Keyset

| Feature | OFFSET | Keyset / Cursor |
|---|---|---|
| Simplicity | High | Medium |
| Page-number navigation | Yes | No/limited |
| Deep pagination | Less efficient | Generally better |
| Stable under changes | Weaker | Stronger with stable ordering |
| Large datasets | Can become expensive | Better suited |
| Cursor handling | Not required | Required |

## Interview Takeaway

For small datasets and simple interfaces, OFFSET pagination is often sufficient.

For large, frequently changing datasets and feeds where clients usually request the next page, keyset/cursor pagination is often a better choice.

---
