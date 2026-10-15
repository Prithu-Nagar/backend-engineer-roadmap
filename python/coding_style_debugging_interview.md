# Python Coding Style and Debugging — Interview Questions

Use these prompts to explain how you write maintainable Python and debug failures systematically in backend services.

## Coding Style and Maintainability

### 1. What makes Python code maintainable?
Prefer clear names, small functions with focused responsibilities, explicit dependencies, type hints at useful boundaries, and consistent formatting. Optimize for readability first; use abstractions when they reduce complexity rather than merely hiding a few lines.

### 2. How do you structure error handling?
Catch exceptions where the application can recover, add useful context, and preserve the original cause with exception chaining when translating errors. Avoid broad `except Exception` blocks that silently continue or hide programming defects.

```python
def load_user(repository, user_id: int):
    try:
        return repository.get(user_id)
    except RepositoryUnavailableError as exc:
        raise UserLookupError(f"Could not load user {user_id}") from exc
```

Define domain-specific exceptions before using this example in an application.

### 3. When should you add type hints?
Use them for public functions, domain models, service boundaries, and complex data structures where they clarify contracts. Type hints support static analysis but do not validate untrusted runtime input by themselves.

### 4. How do you avoid mutable default argument bugs?
Use `None` as a sentinel and create a fresh mutable object inside the function.

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

### 5. How do you review a pull request?
Check correctness, edge cases, naming, complexity, security, logging, compatibility, tests, and operational impact. Ask for a small reproducible test when behavior is unclear; avoid style-only feedback that conflicts with the team's agreed formatter or linter.

## Debugging Method

### 6. Walk through a production bug investigation.
1. Establish impact, scope, start time, and affected endpoints or users.
2. Check recent deployments, configuration changes, dependency health, and alerts.
3. Reproduce safely using sanitized data and a representative environment.
4. Follow request/correlation IDs across logs and traces.
5. Form a hypothesis and test one change at a time.
6. Mitigate safely, verify recovery, and record evidence.
7. Add a regression test and follow-up actions.

### 7. How do you debug an intermittent failure?
Capture structured context and relevant timings, identify concurrency or dependency boundaries, and preserve enough evidence to reproduce the failure. Avoid adding sensitive payloads or secrets to logs. Use deterministic tests, controlled clocks, and synchronization primitives where appropriate.

### 8. What is the difference between debugging and profiling?
Debugging finds incorrect behavior; profiling measures resource use and helps locate performance bottlenecks. A slow endpoint should be measured before optimizing, while an incorrect result requires checking inputs, invariants, and control flow.

### 9. What do you do when a bug cannot be reproduced locally?
Compare runtime versions, environment variables, feature flags, data shape, permissions, traffic, and dependency versions. Improve observability and build a minimal reproduction from sanitized evidence rather than assuming production is behaving randomly.

## Interview Scenarios

- A deployment causes elevated 500 responses. What do you check first?
- A function passes unit tests but fails under concurrent requests. How do you isolate shared state?
- A fix resolves the symptom but increases latency. How do you validate the trade-off?
- A linter reports many issues in legacy code. How do you introduce enforcement without hiding new defects?

Explain the reasoning, evidence, and trade-offs behind each decision rather than listing tools alone.
