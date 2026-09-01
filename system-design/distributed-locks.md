# Distributed Locks

Day 32 introduces distributed locks as a coordination mechanism for work that
may be executed by multiple application instances.

## What Is a Distributed Lock?

A distributed lock coordinates access to a shared resource across processes or
machines.

```text
Worker A ──┐
Worker B ──┼──> Lock Service ──> Shared Resource
Worker C ──┘
```

The goal is to ensure that only an allowed number of workers enter a critical
section at the same time.

## Why Is a Local Lock Not Enough?

A Python `threading.Lock` only coordinates threads that share the same process.
It cannot coordinate two application instances running on different machines.

```text
Instance A                 Instance B
threading.Lock             threading.Lock
     |                          |
     +------ independent -------+
```

A distributed lock requires a shared coordination system that all participating
instances can reach.

## Basic Lifecycle

```text
Acquire
   |
   v
Critical section
   |
   v
Release
```

A production implementation should also consider ownership, expiration,
failure handling, and what happens when the lock holder disappears.

## Lease / TTL

A lock can use a lease with an expiration time so that a crashed worker does
not hold the lock forever.

```text
Acquire lock
    |
    v
Lease active
    |
    +---- refresh while work continues
    |
    v
Release / expire
```

The lease duration must be chosen carefully. A lease that is too short can
expire while work is still running; a lease that is too long can delay recovery
from failures.

## Ownership

A lock should have an identifiable owner or token.

A worker should release a lock only when it still owns that lock. Otherwise a
slow worker could accidentally release a newer lock acquired after its own
lease expired.

## Failure Scenarios

### Worker Crash

The worker disappears while holding the lock. A lease/TTL can allow the lock to
be reclaimed after expiration.

### Lock Service Failure

If the coordination service becomes unavailable, workers need an explicit
failure policy rather than assuming the lock was acquired.

### Long Critical Section

Long-running work increases contention and can cause timeouts for other
workers.

### Duplicate Work

A lock reduces concurrent execution but does not automatically make an
operation idempotent. The underlying operation should still be designed so
retries do not corrupt state.

## Database Locks vs Distributed Locks

| Concern | Database Lock | Distributed Lock |
| --- | --- | --- |
| Scope | Database transaction | Across application instances |
| Typical resource | Database rows | Application-level work/resource |
| Coordination system | Database | Shared lock service |
| Transaction integration | Strong | Application-dependent |
| Failure behavior | Database-managed | Must be designed explicitly |

Prefer database transactions and row-level locking when the resource being
protected is already a database state transition. Use a distributed lock when
coordination must span workers or resources beyond one database transaction.

## Design Checklist

1. Define the exact critical section.
2. Identify the lock owner.
3. Set acquisition and lease timeouts.
4. Prevent accidental release by another owner.
5. Keep the critical section short.
6. Decide what happens when the lock service is unavailable.
7. Make the underlying operation idempotent where possible.
8. Monitor contention, acquisition failures, and lock duration.

## Interview Questions

1. Why can `threading.Lock` not coordinate multiple application instances?
2. What problem does a lock TTL solve?
3. Why is lock ownership important?
4. What happens if a worker crashes while holding a lock?
5. When would a database row lock be preferable to a distributed lock?
6. Does a distributed lock eliminate the need for idempotency?
