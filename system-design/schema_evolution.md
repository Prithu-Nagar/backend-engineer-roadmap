# Schema Evolution

Day 29 focuses on evolving database and API schemas without breaking clients or
older application instances during deployment.

## Why Schema Evolution Matters

Backend systems rarely change all components at exactly the same moment.
Rolling deployments, independently deployed services, and older clients can
cause multiple schema versions to coexist.

Schema evolution should therefore preserve compatibility during the transition.

## Expand-and-Contract

A reliable migration pattern is:

```text
Current Schema
     |
     v
Expand
(add compatible fields)
     |
     v
Deploy compatible code
     |
     v
Migrate / backfill data
     |
     v
Switch clients and services
     |
     v
Contract
(remove obsolete fields)
```

The key rule is to avoid making the old application invalid before the new
application is fully deployed.

## Backward Compatibility

A change is backward compatible when existing consumers can continue to operate
while the new version is introduced.

Examples:

- Adding an optional API response field.
- Adding a nullable database column.
- Supporting old and new field names during a migration.
- Introducing a new endpoint while keeping the old endpoint temporarily.

Risky changes include:

- Removing a response field immediately.
- Renaming a required field without a compatibility period.
- Making an existing optional field required without coordinating consumers.
- Dropping a database column while old application instances still reference it.

## Database Migration Sequence

For a database-backed service:

1. Expand the schema.
2. Deploy code that supports both versions.
3. Backfill or transform existing data.
4. Switch reads and writes to the new representation.
5. Verify all application instances and consumers use the new schema.
6. Contract the obsolete schema in a later deployment.

## API Schema Evolution

For APIs, prefer additive changes when possible.

```text
v1 Client ----               +----> Compatible API
v2 Client ----/
```

If a breaking change is unavoidable, consider:

- Explicit API versioning.
- A migration period.
- Deprecation notices.
- Consumer communication.
- Usage monitoring before removal.

## Common Failure Modes

### Breaking During Rolling Deployment

A new server writes a field that an old server does not understand, or an old
server expects a field that the new schema has removed.

**Mitigation:** use additive changes and compatibility windows.

### Unsafe Backfill

A large data transformation overwhelms the database.

**Mitigation:** batch work, monitor load, and run backfills separately from
request-critical traffic where appropriate.

### Premature Cleanup

An obsolete column or endpoint is removed before all consumers migrate.

**Mitigation:** measure usage and delay the contract step until dependencies are
gone.

## Design Checklist

- What consumers depend on the current schema?
- Can the change be additive?
- Will old and new application versions coexist?
- Is the data migration safe at the expected scale?
- How will compatibility be tested?
- How will deprecated fields be monitored?
- When is the contract step safe?

Schema evolution is successful when the system can change incrementally without
turning deployment timing into a correctness dependency.
