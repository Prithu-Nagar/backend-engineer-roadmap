# Expense Tracker API

Day 31 starts the Expense Tracker project for the Databases & Distributed
Systems phase.

> **Current status (Day 31):** Requirements are defined. Database schema and
> CRUD implementation are planned for Day 32.

## Goal

Build a backend API for recording, categorizing, and reviewing personal
expenses while applying database-oriented backend engineering practices.

## Core Requirements

### Create Expense

The API should accept:

- Amount
- Category
- Description
- Expense date

The API should return:

- Expense ID
- Stored expense details
- Creation metadata

### List Expenses

The API should support:

- Listing expenses
- Filtering by category
- Filtering by date range
- Stable ordering
- Pagination

### Retrieve Expense

A request for a specific expense should return its stored details or a
`404 Not Found` response when the record does not exist.

### Update Expense

The API should allow supported expense fields to be updated while preserving
the record identity and audit metadata.

### Delete Expense

The API should remove an expense only when the requested record exists.

## Data Requirements

The initial relational model should support:

- Unique expense identifiers
- Monetary amounts
- Categories
- Descriptions
- Expense dates
- Creation timestamps
- Update timestamps

The schema should use appropriate constraints and indexes for common lookup
patterns.

## API Expectations

The service should provide:

- Clear HTTP status codes
- Request validation
- Consistent JSON responses
- Parameterized database access
- Transaction boundaries around multi-step writes

## Non-Functional Requirements

The project should evolve toward:

- Safe transaction handling
- Connection pooling
- Query efficiency
- Testability
- Structured error handling
- Observability
- Production-oriented configuration

---

## Day 31 Scope

Day 31 focuses only on requirements and project boundaries.

Planned next step:

- **Day 32:** Database schema + CRUD implementation

The project should grow incrementally without replacing or removing earlier
roadmap projects.

---

## Day 32 — Database Schema + CRUD

Day 32 implements the first database layer for the Expense Tracker.

Added:

- `schema.sql`
- `crud.py`

### Database Schema

The schema defines an `expenses` table with:

- Auto-generated expense ID
- Positive monetary amount
- Category
- Optional description
- Expense date
- Creation and update timestamps
- Category/date index
- Expense-date index

### CRUD Layer

`crud.py` uses SQLAlchemy 2.x ORM models and an injected `Session`.

Supported operations:

- Create an expense
- Retrieve an expense by ID
- List expenses with category/date filters
- Apply stable limit/offset pagination
- Update supported fields
- Delete an expense

The CRUD functions call `flush()` rather than committing internally. This keeps
transaction ownership at the request/service boundary and allows multiple
operations to participate in one transaction.

### Transaction Boundary

The application layer should own the transaction lifecycle:

```text
Request
   |
   v
Open Session / transaction
   |
   +--> CRUD operation(s)
   |
   +--> commit on success
   |
   +--> rollback on failure
   |
   v
Close Session
```

This design keeps database work composable and prepares the project for the
transaction, concurrency, and reliability topics covered later in the roadmap.

---

## Day 33 — Background Aggregation

Day 33 adds an aggregation workload that can be executed as background work.

Added:

- `background_aggregation.py`

The aggregation function supports:

- Start and end date filtering
- Grouping by expense category
- `SUM` aggregation of expense amounts
- Stable category ordering
- Injected SQLAlchemy `Session` usage

The function does not commit or close the session. Transaction and session
lifecycle remain owned by the surrounding application or worker boundary.

---

## Day 34 — Async Processing

Day 34 adds an asynchronous processing boundary for Expense Tracker
aggregation work.

Added:

- `async_processing.py`

The worker provides:

- An `asyncio.Queue` for aggregation jobs
- Async producer/consumer coordination
- Explicit queue completion tracking
- Clean worker shutdown
- `asyncio.to_thread()` for blocking handlers

The existing `background_aggregation.py` remains responsible for the database
aggregation logic. The new processing layer keeps synchronous database work
out of the event loop and provides a clear path for later integration with a
durable worker system.
