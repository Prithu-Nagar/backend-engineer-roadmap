# LLD — Factory and Strategy Patterns

## Goal

Use Factory and Strategy patterns to keep object creation and interchangeable
business behavior explicit without coupling application code to concrete
implementations.

## Factory Pattern

A Factory centralizes creation decisions when the caller should not need to
know which concrete implementation to instantiate.

```text
Application Service
        |
        v
  Report Factory
    /        \
   v          v
Category    Total
Strategy    Strategy
```

The factory should keep supported types explicit and reject unknown types
rather than silently falling back to an unintended implementation.

## Strategy Pattern

Strategy encapsulates a family of interchangeable algorithms behind one
contract.

For an Expense Tracker, report generation can vary without changing the
service that coordinates the use case:

```text
ExpenseReportService
        |
        v
ReportStrategy
   /          \
  v            v
Category     Total
Summary      Summary
```

The service selects behavior through a stable interface instead of branching on
implementation-specific details throughout the application.

## Combined Use

Factory and Strategy complement each other:

1. The application receives a report type.
2. The Factory creates the matching Strategy.
3. The application service invokes the Strategy contract.
4. The concrete calculation remains isolated from the service.

This is useful when the number of interchangeable behaviors is expected to grow
and each behavior has a clear, testable boundary.

## Backend Implications

- Keep factories close to composition/configuration boundaries.
- Keep strategies focused on one variation of a business rule.
- Prefer explicit registration over large conditional branches.
- Validate unsupported strategy types early.
- Inject factories when tests need deterministic or custom construction.
- Do not introduce a pattern solely for indirection; the abstraction should
  justify its maintenance cost.

## Trade-offs

Factory and Strategy add classes and interfaces, which can make a small feature
feel heavier. They become more useful when implementations change independently,
when multiple variants are selected at runtime, or when the behavior needs to be
tested independently.

## Review Checklist

- Is object creation separated from application policy where appropriate?
- Does each Strategy implement the same behavioral contract?
- Can a new Strategy be added without rewriting the service?
- Does the Factory reject unsupported variants explicitly?
- Are the abstractions small and owned by the consumer that needs them?
- Is the pattern reducing coupling rather than adding ceremony?
