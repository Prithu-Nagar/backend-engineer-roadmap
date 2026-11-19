# Rate Limiter Project

## In-process token bucket

The project now includes a runnable, thread-safe in-process token-bucket
implementation in `token_bucket.py`.

- Configurable bucket capacity and refill rate (tokens per second).
- Injectable clock for deterministic tests and reproducible behavior.
- Per-key buckets with independent state.
- Atomic read/refill/consume decisions between threads in one process.
- Remaining-token and retry-after values in every decision.
- Input validation and explicit reset support.

Run the demo from the repository root:

```bash
python projects/rate-limiter/demo.py
```

Run the focused tests:

```bash
python -m pytest projects/rate-limiter/tests -q
```

The implementation is process-local. Separate workers or hosts do not share
bucket state; the Redis-backed atomic variant, TTL behavior, and distributed
concurrency assumptions are the next milestone. The existing design document
retains the shared-store and failure-policy architecture for that extension.

## Design reference

`design_pseudocode.md` describes the intended Redis-backed atomic design,
HTTP response contract, failure policy, and operational trade-offs. The
pseudocode is not presented as a completed Redis integration.
