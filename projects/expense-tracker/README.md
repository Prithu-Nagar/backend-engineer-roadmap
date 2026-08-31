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

## Day 31 Scope

Day 31 focuses only on requirements and project boundaries.

Planned next step:

- **Day 32:** Database schema + CRUD implementation

The project should grow incrementally without replacing or removing earlier
roadmap projects.
