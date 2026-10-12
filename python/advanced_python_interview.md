# Advanced Python Interview Questions

Use these prompts to explain behavior, demonstrate a small example, and discuss when each feature is useful in backend code.

## Decorators

### 1. What is a decorator?
A decorator is a callable that accepts a function or class and returns a replacement or wrapper. The `@decorator` syntax applies it when the function or class is defined.

```python
from functools import wraps
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def measure_time(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = perf_counter() - started
            print(f"{func.__name__}: {elapsed:.6f}s")

    return wrapper
```

### 2. Why use `functools.wraps`?
It preserves useful metadata such as the wrapped function's name, docstring, annotations, and `__wrapped__` reference. Without it, logs, documentation, and introspection may expose the wrapper instead of the original function.

### 3. How do decorators with arguments work?
Use an outer function to capture configuration, return a decorator, and have that decorator return the wrapper. Be explicit about the extra nesting and test both the configured and default behavior.

### 4. What are common risks?
- Accidentally changing the function signature or metadata.
- Hiding exceptions or changing return semantics.
- Adding surprising side effects or unbounded logging.
- Applying a decorator in the wrong order when several decorators are stacked.

## Generators and Iterators

### 5. What is the difference between an iterable, iterator, and generator?
An iterable can produce an iterator; an iterator implements `__iter__()` and `__next__()`; a generator is an iterator commonly created by a function containing `yield`. Generators produce values lazily and retain execution state between yields.

### 6. When are generators useful in backend services?
They can process large files, database result streams, or paginated records incrementally, avoiding the memory cost of materializing every item. Resource lifetime and cleanup still need deliberate handling.

```python
from collections.abc import Iterable, Iterator


def positive_values(values: Iterable[int]) -> Iterator[int]:
    for value in values:
        if value > 0:
            yield value
```

### 7. What should you know about generator exhaustion?
Once a generator raises `StopIteration`, it is exhausted. Create a new generator by calling its generator function again if another pass is required.

## Context Managers

### 8. What does a context manager guarantee?
The `with` statement calls `__enter__()` and ensures `__exit__()` is invoked when the block exits, including when an exception occurs. It is commonly used for files, locks, transactions, and temporary state.

### 9. How can you implement one with `contextlib.contextmanager`?
Place setup before `yield` and cleanup in `finally`. Exceptions from the body are thrown at the `yield` point; re-raise them unless intentionally suppressing them.

```python
from contextlib import contextmanager
from collections.abc import Iterator


@contextmanager
def managed_resource() -> Iterator[str]:
    resource = "opened"
    try:
        yield resource
    finally:
        # Release the resource here.
        pass
```

### 10. How do context managers help with database transactions?
They make commit/rollback and connection cleanup explicit. Verify the behavior of the specific database library: a generic context manager does not automatically imply the same transaction semantics across libraries.

## Interview Checklist

- Explain the difference between decoration time and call time.
- Preserve wrapper metadata and type information where practical.
- Compare lazy iteration with list materialization.
- Explain generator exhaustion and cleanup.
- Describe exception propagation and resource release in a `with` block.
- Give one concrete backend use case for each feature.
