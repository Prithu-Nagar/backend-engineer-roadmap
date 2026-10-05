# Rate Limiter Project

## Day 66

Day 66 adds a design-only Rate Limiter milestone to the project portfolio. The
artifact turns the Rate Limiter HLD into an interview-ready design and
pseudocode exercise without introducing a framework-specific implementation.

Added:

- `design_pseudocode.md`

The design covers:

- Token-bucket enforcement
- Per-user, tenant, API-key, and route-oriented keys
- Atomic shared state using Redis semantics
- Policy configuration and versioning
- Failure behavior and retry handling
- Capacity planning and key-cardinality concerns
- Observability and operational trade-offs

The artifact is intentionally design-first. A production implementation would
still require framework integration, load testing, operational configuration,
and a clear product-level decision about fail-open versus fail-closed behavior.
