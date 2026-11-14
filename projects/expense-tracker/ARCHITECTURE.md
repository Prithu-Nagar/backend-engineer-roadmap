# Expense Tracker — Local MVP Architecture

## Current boundary

The repository has an owner-scoped SQLAlchemy persistence layer, reporting
queries, and an in-process asynchronous aggregation worker. It does **not**
yet expose an integrated HTTP API. The Day 14 Compose target is therefore a
runnable CLI demonstration, not an API deployment.

## Execution flow

```text
Docker Compose / local Python
          |
          v
       demo.py
          |
          +--> SQLAlchemy engine + session factory
          |          |
          |          +--> SQLite database volume
          |          +--> users / expenses tables
          |
          v
  AsyncAggregationWorker
          |
          v
   asyncio.Queue (process-local)
          |
          v
 create_aggregation_handler
          |
          v
 asyncio.to_thread + per-job Session
          |
          v
 aggregate_by_category
          |
          v
 owner-scoped Decimal totals
```

## Transaction and session ownership

- The demo seeds its user and sample expense inside one
  `sessionmaker.begin()` transaction.
- CRUD helpers only flush; they never commit or close a caller-owned session.
- A failed write must roll back the complete surrounding transaction.
- The aggregation handler creates and closes a separate session for each job.
- The worker forwards a job exception to that job's future and continues
  consuming later jobs.

## Failure behavior and limitations

The worker is in-memory and process-local. A process exit loses queued jobs;
there is no durable broker, retry policy, HTTP job endpoint, or multi-worker
coordination. SQLite is used only to make the local demo self-contained. A
PostgreSQL-backed deployment and an integrated HTTP application remain future
work.

The Compose service exits after printing the aggregation result. Its named
volume preserves the SQLite database between runs.
