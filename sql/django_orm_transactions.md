# Django ORM Transactions

Day 25 applies database transaction concepts through Django's ORM.

## Why Transactions Matter

A transaction groups related database operations into one unit of work. This
prevents a partially completed operation from leaving the application in an
unexpected state.

## `transaction.atomic()`

Django provides `transaction.atomic()` as the primary ORM transaction boundary.

```python
from django.db import transaction

with transaction.atomic():
    account.balance -= amount
    account.save(update_fields=["balance"])

    ledger_entry.save()
```

If an exception escapes the block, Django rolls the transaction back. If the
block completes successfully, the transaction commits.

## Nested Atomic Blocks

Nested `atomic()` blocks use savepoints by default. This allows an inner unit
of work to be rolled back without necessarily discarding the surrounding
transaction.

```python
with transaction.atomic():
    update_main_record()

    try:
        with transaction.atomic():
            update_optional_record()
    except ValueError:
        handle_optional_failure()
```

## Row-Level Locks

When concurrent requests must not modify the same row simultaneously,
`select_for_update()` can be combined with an atomic transaction.

```python
with transaction.atomic():
    account = (
        Account.objects
        .select_for_update()
        .get(pk=account_id)
    )
    account.balance -= amount
    account.save(update_fields=["balance"])
```

The row remains locked until the transaction ends.

## ORM Transactions Checklist

- Keep related writes inside the same transaction boundary.
- Roll back when a required operation fails.
- Use `select_for_update()` when a read-then-write operation needs row locking.
- Keep transactions short to reduce lock contention.
- Do not perform slow external network calls inside a database transaction.
- Understand the database's isolation level and locking behavior.

## Backend Use Cases

Transactions are especially useful for:

- Payments and ledger updates
- Inventory changes
- Order creation
- Account transfers
- Multi-table writes
- Maintaining application invariants
