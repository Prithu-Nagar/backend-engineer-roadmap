# Clean Code and Code Review Checklist

## Day 66

This checklist provides a repeatable review pass for Python backend code. The
goal is to improve readability, correctness, maintainability, and operational
safety without turning every review into a stylistic rewrite.

---

## 1. Correctness

- Does the implementation satisfy the stated behavior?
- Are boundary conditions handled explicitly?
- Are invalid inputs rejected at the correct boundary?
- Are exceptions meaningful and narrow enough to be actionable?
- Is mutable state changed only where intended?
- Are retryable and non-retryable failures distinguished?

---

## 2. Naming and Readability

- Do names describe intent rather than implementation details?
- Are functions and classes small enough to understand locally?
- Are boolean names phrased as predicates where appropriate?
- Are comments explaining why rather than restating what the code does?
- Is the control flow easy to follow without excessive nesting?

---

## 3. Design and Maintainability

- Does each class or function have a clear responsibility?
- Are domain rules separated from I/O and framework code?
- Are dependencies explicit and replaceable during tests?
- Is composition preferred when inheritance does not add real value?
- Are public contracts stable and documented?
- Is duplicated business logic actually shared where appropriate?

---

## 4. Python Quality

- Are type hints present at public boundaries?
- Are `None` and optional values handled intentionally?
- Are context managers used for resources that need deterministic cleanup?
- Are comprehensions used only when they remain readable?
- Are generators used when streaming behavior is useful?
- Are mutable default arguments avoided?
- Are imports minimal, ordered, and unused-import free?

---

## 5. Error Handling

- Are exceptions specific enough for callers to react correctly?
- Is broad `except Exception` avoided unless it is an explicit boundary?
- Is useful context preserved when an exception is translated?
- Are errors logged once at an appropriate ownership boundary?
- Does the code avoid leaking secrets or sensitive request data in errors?

---

## 6. API and Backend Boundaries

- Is validation performed before business logic executes?
- Are request and response models separated from domain objects when needed?
- Are API changes backward compatible or explicitly versioned?
- Are timeout, retry, and idempotency behaviors defined for external calls?
- Are pagination, filtering, and ordering contracts deterministic?

---

## 7. Performance

- Is the algorithm appropriate for the expected input size?
- Are database queries bounded and index-aware?
- Are N+1 query patterns avoided?
- Is repeated expensive work cached only when correctness permits it?
- Are connection, thread, process, and async-task counts bounded?
- Has optimization been driven by measurements rather than assumptions?

---

## 8. Testing

- Are normal, boundary, and failure paths covered?
- Does the test assert behavior rather than implementation details?
- Are external dependencies replaced with deterministic test doubles?
- Are retries and idempotency tested where they affect behavior?
- Does the test suite remain isolated and order-independent?

---

## 9. Review Outcome

Before approving a change, record:

1. **Correctness:** behavior is correct and edge cases are considered.
2. **Design:** responsibilities and dependencies are clear.
3. **Compatibility:** existing consumers are not silently broken.
4. **Performance:** likely bottlenecks are understood and measurable.
5. **Testing:** important behavior has deterministic coverage.
6. **Operations:** logging, metrics, timeouts, and failure behavior are clear.

A good review should identify the highest-risk issue first instead of producing
an unprioritized list of minor style preferences.
