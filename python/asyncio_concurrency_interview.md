# AsyncIO and Concurrency — Python Interview Questions

Use these questions to explain concurrency choices, event-loop behavior, cancellation, and failure handling in backend services.

## AsyncIO Fundamentals

### 1. What problem does `asyncio` solve?
`asyncio` supports concurrent I/O by scheduling coroutines on an event loop. It is useful when a service spends substantial time waiting for network, database, or other asynchronous I/O. It does not automatically make CPU-bound Python code run in parallel.

### 2. What do `async` and `await` mean?
- `async def` defines a coroutine function.
- Calling it creates a coroutine object; it does not execute the coroutine to completion.
- `await` suspends the current coroutine until the awaited operation completes, allowing the event loop to run other ready work.

### 3. What is the difference between a coroutine, a Task, and a Future?
A coroutine describes asynchronous work. A `Task` schedules a coroutine on the event loop and tracks its result. A `Future` represents a result that will become available later and can be completed by asynchronous infrastructure.

### 4. Why can blocking code be harmful inside an async endpoint?
A blocking call occupies the event-loop thread, delaying unrelated tasks. Use an async-compatible client where possible, or move unavoidable blocking work to a thread/process executor with bounded concurrency.

### 5. How do `asyncio.gather()` and `TaskGroup` differ?
`gather()` awaits multiple awaitables and has configurable exception behavior. `TaskGroup` (Python 3.11+) provides structured concurrency: child tasks are scoped to the context manager, and failures trigger coordinated cancellation and exception propagation. Match the choice to the supported Python version and desired failure semantics.

## Concurrency and Performance

### 6. AsyncIO vs threading vs multiprocessing
- **AsyncIO:** many concurrent I/O operations with cooperative scheduling.
- **Threading:** blocking I/O or libraries that do not expose async APIs; shared memory requires synchronization.
- **Multiprocessing:** CPU-bound work that benefits from multiple processes, with serialization and process-management overhead.

Choose based on the workload and library behavior, not on a blanket rule that one model is always faster.

### 7. How do you limit concurrency?
Use a semaphore, bounded queue, connection pool, or worker pool. Bound both active work and queued work; otherwise a burst can create excessive memory use, connection pressure, or downstream overload.

```python
import asyncio

async def fetch_with_limit(items, fetch, limit=10):
    semaphore = asyncio.Semaphore(limit)

    async def bounded_fetch(item):
        async with semaphore:
            return await fetch(item)

    return await asyncio.gather(*(bounded_fetch(item) for item in items))
```

For very large inputs, prefer a bounded producer/consumer queue over creating one task per item.

### 8. How should cancellation be handled?
Cancellation is a control-flow signal. Use `try/finally` for cleanup, release resources with context managers, and normally re-raise `asyncio.CancelledError` after cleanup. Do not swallow cancellation or leave partially completed state without an explicit recovery policy.

### 9. How do timeouts and retries interact?
Set timeouts at dependency boundaries and budget them against the overall request deadline. Retry only transient failures, use bounded attempts with exponential backoff and jitter, and avoid retrying non-idempotent operations unless idempotency is guaranteed.

### 10. How would you test asynchronous code?
Use the project's supported async test integration (for example, pytest-asyncio when configured). Test successful results, exceptions, timeouts, cancellation, concurrency limits, and cleanup. Replace network dependencies with deterministic fakes rather than relying on real services.

## Backend Scenarios

### 11. An async API is slow despite using `async def`. What do you investigate?
- Blocking database or HTTP clients.
- CPU-heavy serialization or computation on the event loop.
- Connection-pool exhaustion and queueing.
- Excessive task creation or unbounded fan-out.
- Missing deadlines, slow dependencies, and tail-latency metrics.

### 12. What metrics are useful?
Track request latency percentiles, event-loop lag, active and queued tasks, connection-pool wait time, timeout/cancellation counts, downstream latency, and error rates. Avoid logging credentials or sensitive payloads.

## Quick Revision

- AsyncIO is cooperative concurrency, not automatic CPU parallelism.
- Every awaited dependency should have deliberate timeout and cancellation behavior.
- Bound concurrency, queues, and retries.
- Prefer structured task lifetimes and deterministic async tests.
