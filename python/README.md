# Python

This directory contains Python concepts and implementations covered throughout the Backend Engineer Roadmap.

The focus is on building strong Python fundamentals for backend development, followed by advanced topics related to concurrency and asynchronous programming.

---

## Topics

### Iterables & Iterators

- Iterables
- Iterators
- `iter()`
- `next()`

### enumerate()

Using `enumerate()` to iterate over collections while tracking indexes.

### zip()

Combining multiple iterables into pairs or groups of related values.

### List Comprehensions

Concise syntax for creating lists from iterable data.

### Dictionary Comprehensions

Concise syntax for creating dictionaries from iterable data.

### Functions

- Function definitions
- Parameters
- Return values
- Default arguments
- Keyword arguments

### *args & **kwargs

Handling variable numbers of positional and keyword arguments.

### Variable Scope

Understanding Python's LEGB scope resolution:

- Local
- Enclosing
- Global
- Built-in

### Lambda Functions

Small anonymous functions commonly used with functional programming patterns.

### First-Class Functions

Functions as first-class objects that can be:

- Assigned to variables
- Passed as arguments
- Returned from other functions

### Higher-Order Functions

Functions that accept other functions as arguments or return functions.

### Nested Functions

Functions defined inside other functions.

### Closures

Functions that retain access to variables from their enclosing scope.

### Decorators

Functions that modify or extend the behavior of other functions.

### Generators

Lazy iteration using:

- `yield`
- Generator functions
- Generator expressions

### Exception Handling

Handling runtime errors using:

- `try`
- `except`
- `else`
- `finally`
- `raise`

### Context Managers

Managing resources safely using:

- `with`
- `__enter__`
- `__exit__`
- `contextlib`

### Threading

Running multiple threads within a process.

Topics include:

- `threading.Thread`
- Thread creation
- Starting threads
- Joining threads
- Shared state
- Race conditions
- Locks

### Multiprocessing

Running work across multiple processes.

Topics include:

- `multiprocessing.Process`
- Process creation
- Starting processes
- Joining processes
- Process isolation
- CPU-bound workloads

---

### AsyncIO vs Threading vs Multiprocessing

Python supports different concurrency models, and each is best suited to different kinds of workloads.

- Threading is often used for I/O-bound tasks.
- Multiprocessing is better for CPU-bound operations.
- AsyncIO is efficient for many concurrent I/O operations with a single event loop.

File: `asyncio_vs_threading_vs_multiprocessing.py`

---

# AsyncIO

AsyncIO provides asynchronous programming capabilities for handling I/O-bound operations efficiently.

Day 11 introduced the fundamentals of asynchronous programming.

Day 12 builds on those fundamentals by working with asyncio tasks, concurrency, timeouts, and cancellation.

---

## AsyncIO Fundamentals

Topics covered:

- Event loop
- Coroutines
- `async`
- `await`
- I/O-bound asynchronous execution
- `asyncio.run()`
- `asyncio.sleep()`

File:

`asyncio_basics.py`

---

## AsyncIO Tasks

Topics covered:

- `asyncio.create_task()`
- `asyncio.gather()`
- Running multiple coroutines concurrently
- Timeouts
- `asyncio.wait_for()`
- `asyncio.TimeoutError`
- Task cancellation
- `asyncio.CancelledError`

File:

`asyncio_tasks.py`

---

## Sequential vs Concurrent Async Execution

Sequential execution waits for each coroutine to finish before starting the next operation.

Concurrent execution schedules multiple coroutines so they can make progress while other coroutines are waiting for I/O.

Example:

Sequential:

Task 1
   ↓
Wait
   ↓
Task 2
   ↓
Wait
   ↓
Complete

Concurrent:

Task 1 ──────────────┐
                     ├── Complete
Task 2 ────────┐     │
               └─────┘

---

## asyncio.create_task()

`asyncio.create_task()` schedules a coroutine to run as an asyncio Task.

Example:

task = asyncio.create_task(fetch_data())

The task can then be awaited later.

This is useful when multiple asynchronous operations should be scheduled before waiting for their results.

---

## asyncio.gather()

`asyncio.gather()` waits for multiple awaitable objects and returns their results.

Example:

results = await asyncio.gather(
    task_1,
    task_2,
)

The returned results preserve the order of the awaitables passed to `gather()`.

---

## Timeouts

Long-running asynchronous operations can be limited using:

`asyncio.wait_for()`

Example:

result = await asyncio.wait_for(
    fetch_data(),
    timeout=2,
)

If the operation exceeds the timeout, `asyncio.TimeoutError` is raised.

Timeouts are useful for preventing an application from waiting indefinitely for an external service.

---

## Task Cancellation

An asyncio task can be cancelled using:

task.cancel()

The coroutine can respond to cancellation through `asyncio.CancelledError`.

Cancellation is useful when:

- A timeout occurs
- A request is disconnected
- A task is no longer required
- An application is shutting down

---

# AsyncIO vs Threading vs Multiprocessing

| Feature | AsyncIO | Threading | Multiprocessing |
| --- | --- | --- | --- |
| Execution model | Cooperative | Concurrent threads | Separate processes |
| Best suited for | I/O-bound work | I/O-bound work | CPU-bound work |
| Memory | Shared process | Shared process | Separate processes |
| Context switching | Cooperative | OS-managed | OS-managed |
| CPU parallelism | No | Limited by GIL for Python code | Yes |
| Typical use | Network I/O | Blocking I/O | CPU-heavy workloads |

---

# Learning Approach

For Python topics:

1. Understand the underlying language feature.
2. Implement a small example.
3. Understand common use cases.
4. Analyze trade-offs.
5. Apply the concept to backend development.
6. Practice with realistic examples.
7. Review how the concept interacts with other Python features.

The goal is to build Python knowledge that can be directly applied to production backend systems.
