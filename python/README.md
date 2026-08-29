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

### Type Hints

Type hints make Python code more explicit, easier to read, and better supported by IDE tooling and static analysis.

Topics include:

- Function annotations
- Built-in generics like `list[int]` and `dict[str, int]`
- `Optional[T]`
- Return type annotations
- Improved maintainability and editor help

File: `type_hints.py`

Type hints are especially useful in backend services when modeling inputs, outputs, and domain data.

---

## Dataclasses

Day 15 introduces dataclasses for defining simple classes with less boilerplate.

Dataclasses automatically generate common methods like `__init__`, `__repr__`, and `__eq__`.

Topics include:

- `@dataclass` decorator
- Field definitions
- Automatic method generation (`__init__`, `__repr__`, `__eq__`)
- Field defaults and `field(default_factory=...)`
- Post-initialization with `__post_init__`
- Immutable dataclasses with `frozen=True`
- Comparison methods with `order=True`
- Type hints integration

File: `dataclasses.py`

Dataclasses are particularly useful for:

- Defining data structures
- Request/response models in APIs
- Configuration objects
- Domain models in backend services
- Reducing boilerplate code while maintaining readability

---

## Day 19 — OOP Design

Day 19 reviews object-oriented design with a backend-engineering focus.

Topics include:

- Composition vs inheritance
- Encapsulation
- Abstraction
- Polymorphism
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle
- Dependency injection

File:

`oop_design.py`

The examples emphasize composition and dependency inversion because
these patterns make backend components easier to test, replace, and extend.

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

```text
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
```

---

## asyncio.create_task()

`asyncio.create_task()` schedules a coroutine to run as an asyncio Task.

Example:

```python
task = asyncio.create_task(fetch_data())
```

The task can then be awaited later.

This is useful when multiple asynchronous operations should be scheduled before waiting for their results.

---

## asyncio.gather()

`asyncio.gather()` waits for multiple awaitable objects and returns their results.

Example:

```python
results = await asyncio.gather(
    task_1,
    task_2,
)
```

The returned results preserve the order of the awaitables passed to `gather()`.

---

## Timeouts

Long-running asynchronous operations can be limited using:

`asyncio.wait_for()`

Example:

```python
result = await asyncio.wait_for(
    fetch_data(),
    timeout=2,
)
```

If the operation exceeds the timeout, `asyncio.TimeoutError` is raised.

Timeouts are useful for preventing an application from waiting indefinitely for an external service.

---

## Task Cancellation

An asyncio task can be cancelled using:

```python
task.cancel()
```

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

## Python Memory Model

Day 16 covers how Python variables reference objects in memory.

Topics include:

- Object references
- Assignment and aliasing
- Mutability
- Identity vs equality
- `is` vs `==`
- Shallow copy
- Deep copy
- `copy.copy()`
- `copy.deepcopy()`

**File:** `memory_model.py`

---
## Iterators and Generators

- Iterator patterns
- Generator patterns
- Lazy evaluation
- Generator pipelines

**File:** `iterator_generator_patterns.py`

---

### Day 18 — Context Managers + Decorators Revision

Day 18 revisits Context Managers and Decorators with emphasis on
their practical use in backend applications.

Context managers provide reliable setup and cleanup around resources.

Decorators allow cross-cutting behavior such as:

- Logging
- Authorization
- Validation
- Timing
- Error handling

The Task Manager project applies these concepts alongside generator
pipelines and standardized error handling.

---

Understanding references and mutability is important when working with:

- Lists
- Dictionaries
- Nested objects
- Function arguments
- Shared state
- API data structures

---

# Day 22 — AsyncIO HTTP and Database Workloads

Day 22 applies AsyncIO to backend-style I/O workloads.

Topics include:

- Async HTTP operations
- Async database operations
- Concurrent independent I/O
- `asyncio.create_task()`
- `asyncio.gather()`
- Avoiding blocking synchronous work in async handlers
- Choosing async-compatible clients and drivers

File:

`asyncio_http_database.py`

A common backend pattern is:

```text
Request
   |
   +----> Async HTTP call
   |
   +----> Async database query
   |
   v
Combine results
   |
   v
Response
```

The important distinction is that AsyncIO improves concurrency for operations
that spend time waiting on I/O. It does not make CPU-bound Python code
automatically execute in parallel.

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

---

# Day 23 — Packaging, Virtual Environments & Dependency Management

Day 23 introduces the practical Python packaging workflow used to keep
backend projects isolated and reproducible.

Topics include:

- Virtual environments with `venv`
- Dependency installation with `pip`
- Dependency snapshots with `requirements.txt`
- Modern packaging configuration with `pyproject.toml`
- Dependency isolation and reproducibility
- Keeping development and runtime environments predictable

File:

`packaging_basics.py`

Day 23 also includes a small dependency example:

`requirements.txt`

A typical workflow is:

```text
Create .venv
    |
    v
Activate environment
    |
    v
Install dependencies
    |
    v
Record dependency versions
    |
    v
Recreate environment elsewhere
```

The important goal is that the application should not depend on whatever
packages happen to be installed globally on the developer's machine.

---

## Day 24 — Configuration Management

Day 24 introduces configuration management for backend services.

Topics include:

- Environment variables
- Environment-specific configuration
- Required settings
- Secret handling
- Avoiding hard-coded credentials
- Configuration validation at application startup

File:

`configuration_management.py`

The example keeps secrets outside source code and raises a clear configuration
error when a required secret is missing.


## Day 25 — Debugging & Profiling Basics

Day 25 focuses on a practical debugging workflow for backend Python code.

Topics include:

- Reading tracebacks from the bottom up
- Identifying the exception type and failing line
- Reproducing failures with small inputs
- Using `timeit` for focused timing measurements
- Using `cProfile` and `pstats` to locate expensive functions
- Measuring before optimizing

File:

`debugging_and_profiling.py`

The goal is to separate correctness debugging from performance profiling and
to use measurements rather than assumptions when investigating slow code.

---

## Day 26 — Performance Profiling

Day 26 focuses on measuring Python performance before making optimization
decisions.

Topics include:

- Performance profiling
- `timeit` for focused timing
- `cProfile` for function-level profiling
- `pstats` for reading profiler output
- Measuring representative workloads
- Avoiding premature optimization

File:

`debugging_and_profiling.py`

The profiling workflow complements Day 25 debugging work: first establish
correctness, then measure the actual performance bottleneck.

---

## Day 27 — FastAPI Typing & Pydantic Models

Day 27 connects Python type hints with FastAPI request and response contracts.

Topics include:

- Type annotations in FastAPI endpoints
- `Annotated`
- Pydantic `BaseModel`
- `Field` constraints
- Typed request bodies
- Typed response models
- Query-parameter validation

File:

`fastapi_typing_pydantic.py`

The goal is to make API contracts explicit so invalid input is rejected before
business logic runs and generated API documentation reflects the declared
schema.

---

## Day 28 — Async FastAPI

Day 28 connects Python `async`/`await` and concurrency concepts to FastAPI
request handling.

Topics include:

- `async def` FastAPI endpoints
- Awaiting I/O-bound operations
- `asyncio.gather()` for independent work
- Avoiding blocking operations in the async request path
- When synchronous endpoints are still appropriate

File:

`async_fastapi.py`

The example uses simulated I/O so the async control flow can be studied
without requiring an external service.

---

## Day 29 — Testing Async Code, Mocks & Dependency Overrides

Day 29 focuses on testing asynchronous Python code and isolating dependencies
during backend tests.

Topics include:

- Async test execution
- `AsyncMock`
- Await assertions
- Mocking asynchronous I/O
- Deterministic dependency behavior
- FastAPI dependency overrides

File:

`async_testing.py`

The example uses `AsyncMock` to test an async dependency without performing
real network I/O.
