# Python Concurrency — Coding Interview Practice

Use these exercises to explain concurrency choices and write code that remains correct under load. Prefer small, testable functions and state the assumptions behind each answer.

## Exercise 1: Bound Concurrent I/O

**Prompt:** Fetch 100 URLs using `asyncio`, but never allow more than 10 requests to be in flight.

**Expected approach:**
- Use an async HTTP client with a shared connection pool.
- Guard requests with `asyncio.Semaphore(10)` or use a bounded worker queue.
- Set connect/read timeouts and handle expected network errors.
- Reuse the client instead of creating one client per request.
- Cancel or await outstanding tasks during shutdown.

**Follow-up:** Explain why `asyncio.gather()` over thousands of unbounded tasks may cause memory pressure even when the requests are I/O-bound.

## Exercise 2: Thread-Safe Shared Counter

**Prompt:** Multiple threads increment a shared counter. Explain why `counter += 1` should not be assumed to be a safe synchronization primitive.

**Expected approach:**
- Protect the read-modify-write operation with `threading.Lock`.
- Keep the critical section small.
- Prefer a queue or message-passing design when workers can send results to one owner.
- Write a stress test that checks the final count, while recognizing that a passing stress test alone does not prove thread safety.

## Exercise 3: CPU-Bound Work

**Prompt:** Process a large collection of independent CPU-heavy records.

**Decision guide:**
- Use ordinary sequential code for small workloads or when overhead dominates.
- Consider `ProcessPoolExecutor` for CPU-bound Python work when process startup and serialization costs are justified.
- Consider threads or `asyncio` for I/O-bound workloads.
- Benchmark representative inputs before choosing a design.

## Exercise 4: Avoid Blocking the Event Loop

**Prompt:** An async endpoint calls a slow synchronous library.

**Expected approach:**
- Prefer an async-native client if available.
- Otherwise move blocking I/O to a thread with `asyncio.to_thread()` where appropriate.
- Do not move CPU-heavy Python code to a thread expecting reliable parallel execution under the standard CPython GIL.
- Set timeouts and propagate cancellation deliberately.

## Exercise 5: Bounded Producer–Consumer Pipeline

**Prompt:** Producers create jobs faster than workers can process them.

**Expected approach:**
- Use a bounded `queue.Queue` for threaded workers or `asyncio.Queue(maxsize=...)` for async workers.
- Define backpressure behavior: block, reject, shed low-priority work, or persist it.
- Decide how errors, retries, shutdown sentinels, and unfinished jobs are handled.
- Avoid retry loops that amplify overload.

## Interview Checklist

- Can you distinguish concurrency from parallelism?
- Can you explain the GIL without claiming it prevents all concurrency?
- Can you identify shared mutable state and its synchronization boundary?
- Can you justify worker limits, timeouts, cancellation, and backpressure?
- Can you explain the failure modes and test strategy?

## Complexity and Trade-Offs

Concurrency does not automatically improve performance. Measure throughput, tail latency, CPU utilization, memory, context-switching overhead, and downstream limits. Bound work at the point where it enters the system.
