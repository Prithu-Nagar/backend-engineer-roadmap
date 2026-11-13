# Expense Tracker MVP Contract

## Purpose and scope

The Expense Tracker MVP records personal expenses and provides reliable
retrieval, filtering, and basic spending summaries. The existing repository
contains useful database and learning modules, but it does not yet contain one
integrated, runnable HTTP application. This contract defines the target
behavior for the next implementation increments; it does not claim that the
API described here is already implemented.

### In scope

- Create, retrieve, list, update, and delete an expense.
- Filter expenses by category and an inclusive expense-date range.
- Stable pagination and deterministic ordering.
- Persist expenses in a relational database.
- Keep writes within an application/service-owned transaction.
- Scope records to the authenticated owner when authentication is integrated.
- Provide category totals for a date range as a basic reporting operation.

### Explicitly out of scope for the MVP

- Multiple wallets or accounts, transfers, recurring expenses, attachments,
  receipt OCR, exchange-rate conversion, and shared household accounts.
- Budgets, recurring expenses, transfers, and shared household accounts.
- A frontend, microservices, and production-scale distributed processing.
- Redis caching or asynchronous aggregation until correctness and measured
  need justify them.

## Domain model

### Expense

| Field | Type | Required | Rules |
|---|---|---:|---|
| `id` | integer | generated | Database primary key; immutable |
| `owner_id` | integer/UUID | authenticated context | Required for owner-scoped access; never trusted from request body |
| `amount` | decimal | yes | Positive; maximum 2 fractional digits; bounded by `NUMERIC(12, 2)` |
| `category` | string | yes | Trimmed, non-empty, maximum 50 characters |
| `description` | string or null | no | Trimmed when present; maximum 255 characters |
| `expense_date` | date | yes | Calendar date in ISO `YYYY-MM-DD` format |
| `created_at` | timestamp | generated | UTC timestamp; immutable |
| `updated_at` | timestamp | generated | UTC timestamp; changes on successful update |

The MVP uses a single configured currency per deployment. Currency conversion
and per-record currency are not part of this contract. The configured currency
must be made explicit in application configuration and documentation before
the API is exposed; do not infer it from a user's locale.

## Category persistence

Categories are independently managed per owner. The persistence layer supports
create, retrieve, list, rename, and delete operations. Category names are
non-empty, limited to 50 characters, and unique within an owner. The expense
record continues to store the category label as defined by the existing MVP
contract; the calling service must use the authenticated owner's context when
performing both category and expense operations.

## Money rules

- Accept monetary input as a decimal string (for example, `"125.50"`), not a
  binary floating-point JSON number.
- Parse with Python `Decimal`; never use `float` for persisted amounts,
  arithmetic, comparisons, or aggregation.
- Reject zero and negative amounts.
- Reject values with more than two fractional digits rather than silently
  rounding them.
- Enforce the database precision represented by `NUMERIC(12, 2)`.
- Persist and aggregate using fixed-point decimal arithmetic.
- Serialize monetary values as strings with exactly two fractional digits.
- Keep currency configuration separate from the numeric amount; do not mix
  currencies in one deployment or aggregate them without an explicit
  conversion design.

## Date and timestamp rules

- `expense_date` is a date-only business value, not a timestamp. Accept and
  return ISO `YYYY-MM-DD`; do not apply timezone conversion to it.
- Date filters use inclusive boundaries: `expense_date >= start_date` and
  `expense_date <= end_date`.
- If both filter bounds are supplied, reject `start_date > end_date`.
- Reject malformed dates; do not silently reinterpret locale-specific formats.
- `created_at` and `updated_at` are audit timestamps stored as timezone-aware
  UTC values. Serialize them as ISO 8601 timestamps with a `Z` or `+00:00`
  offset.
- The application/database clock is authoritative for audit timestamps.
  Clients cannot set or overwrite them.

## API contract

Base path: `/api/v1/expenses`

| Method | Path | Purpose | Success |
|---|---|---|---|
| `POST` | `/api/v1/expenses` | Create an expense | `201 Created` |
| `GET` | `/api/v1/expenses` | List/filter expenses | `200 OK` |
| `GET` | `/api/v1/expenses/{expense_id}` | Retrieve one expense | `200 OK` |
| `PATCH` | `/api/v1/expenses/{expense_id}` | Partially update supported fields | `200 OK` |
| `DELETE` | `/api/v1/expenses/{expense_id}` | Delete an expense | `204 No Content` |
| `GET` | `/api/v1/expenses/summary` | Category totals for a date range | `200 OK` |

### Create request

```json
{
  "amount": "125.50",
  "category": "Food",
  "description": "Lunch",
  "expense_date": "YYYY-MM-DD"
}
```

The authenticated owner is derived from the request's security context. The
client cannot submit `id`, `owner_id`, `created_at`, or `updated_at`.

### List query parameters

- `category`: optional exact category filter.
- `start_date`, `end_date`: optional inclusive ISO date bounds.
- `limit`: default 20, minimum 1, maximum 100.
- `offset`: default 0, minimum 0.

Order results by `expense_date DESC, id DESC` to ensure deterministic ordering
when multiple expenses share a date.

### Response representation

```json
{
  "id": 42,
  "amount": "125.50",
  "category": "Food",
  "description": "Lunch",
  "expense_date": "YYYY-MM-DD",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

The timestamp values above are illustrative only. The summary response returns
a list of `{ "category": "...", "total": "..." }` entries, with each total
serialized as a two-decimal string.

## Validation and error contract

Use one consistent JSON error shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": {
      "amount": "Must be a positive decimal with at most two fractional digits."
    }
  }
}
```

| Status | Meaning |
|---|---|
| `400` | Malformed query/body values or validation failure |
| `401` | Missing or invalid authentication |
| `404` | Expense does not exist or is not visible to the authenticated owner |
| `409` | Conflict that cannot be represented as a validation error |
| `500` | Unexpected server failure; do not expose internal exception details |

Do not reveal whether an expense belongs to another user. Treat a non-owned
record as not found. Database errors must trigger rollback before the error is
translated into an HTTP response.

## Persistence and transaction boundaries

- Keep the relational schema as the source of truth.
- Use `NUMERIC(12, 2)` for amounts and a SQL `DATE` for `expense_date`.
- Add an owner foreign key/index as part of the persistence increment before
  enabling authenticated multi-user access.
- Preserve the existing category/date and date indexes; validate additional
  indexes against actual query patterns.
- The service/request boundary owns commit and rollback. CRUD helpers may
  `flush()` but must not commit or close the caller's session.
- A failed multi-step write is rolled back as one unit.
- Aggregations read persisted values and return decimal totals.

## Repository audit and implementation decisions

The repository already has these reusable pieces:

| Existing module | Audit finding | Decision |
|---|---|---|
| `schema.sql` | PostgreSQL-style `expenses` table, positive amount check, `NUMERIC(12, 2)`, date and category/date indexes; no owner column yet | Retain; extend with ownership when persistence is integrated |
| `crud.py` | SQLAlchemy 2.x model and CRUD helpers; uses `Decimal`, `DATE`, and injected `Session`; helpers flush without committing | Retain as the primary persistence starting point |
| `background_aggregation.py` | SQL aggregation by category and inclusive date bounds; returns `Decimal` totals | Reuse after persistence integration |
| `async_processing.py` | In-process `asyncio.Queue` worker runs owner-scoped aggregation with per-job sessions and result/error reporting | Reuse for local background execution; it is not durable and is not part of the initial HTTP API |
| `caching_layer.py` | Cache-aside example with a separate `float`-based domain object | Do not use as the canonical money model; align only if caching is justified |
| `redis_caching.py` | Redis adapter serializes amounts through `float` | Requires Decimal-safe serialization before production use |
| `architecture_refactor.py` | In-memory repository example uses `float` and caller-supplied IDs | Treat as an architecture exercise, not canonical persistence |
| `lld_design.py` | Reporting Strategy/Factory example uses `float` | Preserve as a pattern exercise; align monetary types before reuse |
| `observability.py`, `reliability.py` | Framework-independent logging and bounded retry examples | Reuse selectively at service/integration boundaries |

There is still no Expense Tracker HTTP application or integrated route set.
Project-specific tests now cover the persistence, reporting, and local worker
modules, but the README must continue to label the overall project as not yet
integrated until the API exists.

## Phase 2 Day 13 boundary

Day 13 connects the in-process worker to the persistent category aggregation
and verifies owner isolation, per-job session lifecycle, and failure
propagation. It intentionally does not add a durable queue, an HTTP job API,
or caching; the existing project has no demonstrated cache need. The worker
and aggregation are runnable modules, not an integrated HTTP application.
