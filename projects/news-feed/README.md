# News Feed

Day 69 design artifact for the News Feed milestone.

The detailed architecture is documented in:

- `architecture.md`

The design focuses on:

- Personalized feed reads
- Fan-out-on-read versus fan-out-on-write
- Hybrid feed generation for high-fan-out authors
- Cursor pagination
- Bounded caching
- Asynchronous feed materialization
- Freshness and eventual consistency
- Scaling and observability
