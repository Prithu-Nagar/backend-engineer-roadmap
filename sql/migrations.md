# Database Migration Strategy

Day 29 focuses on safely evolving a database schema while keeping deployed
application versions compatible during a rollout.

## Goals

A production migration should:

- Be version-controlled and repeatable.
- Preserve existing data.
- Support a safe deployment sequence.
- Avoid breaking older application instances during rolling deployments.
- Keep schema changes observable and reversible where practical.

## Expand-and-Contract Strategy

A common backward-compatible migration uses three stages.

### 1. Expand

Add the new schema without removing the old schema.

Examples:

- Add a nullable column.
- Add a new table.
- Add a new index.
- Add a new column with a safe default when the database supports it efficiently.

### 2. Migrate Application Code

Deploy application code that can work with both the old and new schema.

For a column rename, an application may temporarily read the old column and
write both columns.

### 3. Contract

After all application instances use the new schema, remove the old column or
constraint in a later migration.

```text
Old Schema
    |
    v
Expand Schema
    |
    v
Deploy Compatible Application
    |
    v
Backfill Existing Data
    |
    v
Switch Reads/Writes
    |
    v
Contract Old Schema
```

## Example: Renaming a Column Safely

Instead of immediately running:

```sql
ALTER TABLE users
RENAME COLUMN full_name TO display_name;
```

use a compatibility sequence:

```sql
-- Migration 1: expand
ALTER TABLE users
ADD COLUMN display_name VARCHAR(200);

-- Migration 2: backfill existing rows
UPDATE users
SET display_name = full_name
WHERE display_name IS NULL;
```

The application can then temporarily write both `full_name` and
`display_name`.

After the application no longer depends on `full_name`:

```sql
-- Migration 3: contract
ALTER TABLE users
DROP COLUMN full_name;
```

The exact rollout should be adapted to the database engine, table size,
locking behavior, and deployment strategy.

## Adding a Non-Nullable Column

Adding a required column to an existing table can fail if existing rows have no
value. A safer approach is:

```sql
-- Expand
ALTER TABLE orders
ADD COLUMN status VARCHAR(30);

-- Backfill
UPDATE orders
SET status = 'pending'
WHERE status IS NULL;
```

After application code always supplies `status`, enforce the final constraint:

```sql
ALTER TABLE orders
ALTER COLUMN status SET NOT NULL;
```

## Migration Rules

- Prefer small, focused migrations.
- Do not mix unrelated schema changes in one migration.
- Back up or otherwise protect important production data before risky changes.
- Consider lock duration for large tables.
- Make application rollouts compatible with both schema versions during
  transitions.
- Backfill large datasets in controlled batches when appropriate.
- Validate constraints before enforcing them.
- Record the migration version and deployment state.

## Backward Compatibility Checklist

Before deploying a schema change:

- [ ] Can the previous application version still start?
- [ ] Can the new application version work with the old data?
- [ ] Are reads compatible with both schema versions?
- [ ] Are writes compatible during a rolling deployment?
- [ ] Is existing data preserved?
- [ ] Can the backfill complete without unacceptable load?
- [ ] Is the final constraint safe to enforce?
- [ ] Is the contract step scheduled only after old code is retired?

Schema evolution is an application-deployment concern as well as a database
concern. Safe changes account for the period when multiple application
versions may run at the same time.
