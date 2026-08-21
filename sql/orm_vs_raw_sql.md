# ORM vs Raw SQL

Day 21 compares ORM-based database access with writing SQL directly.

## ORM

An Object-Relational Mapper represents database records as application
objects and translates application operations into SQL.

Typical advantages:

- Productive CRUD development
- Model definitions close to application code
- Reusable query abstractions
- Easier integration with application models

Typical trade-offs:

- Generated SQL can be less obvious
- Complex queries may become harder to express
- Performance still depends on the generated query
- Developers still need SQL knowledge

## Raw SQL

Raw SQL gives the developer direct control over the database query.

Example:

```sql
SELECT id, title
FROM tasks
WHERE status = 'open'
ORDER BY created_at DESC
LIMIT 20;
```

Typical advantages:

- Precise control over the query
- Clear visibility into SQL behavior
- Useful for database-specific features
- Often preferable for complex reporting queries

Trade-offs:

- More SQL to maintain
- Application/database mapping becomes manual
- Parameterization must be handled correctly

## Choosing Between Them

| Situation | Good default |
|---|---|
| Simple CRUD | ORM |
| Standard model queries | ORM |
| Complex reporting query | Raw SQL |
| Database-specific feature | Raw SQL |
| Performance-sensitive query | Measure both; choose based on evidence |

The important backend skill is not choosing one exclusively. It is
understanding the SQL an ORM generates and knowing when direct SQL gives
better control.

## Safety

Never build SQL by concatenating untrusted user input.

Use parameterized queries:

```python
cursor.execute(
    "SELECT id, title FROM tasks WHERE owner_id = %s",
    (owner_id,),
)
```
