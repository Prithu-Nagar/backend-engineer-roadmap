# Python Memory and Performance — Interview Questions

Use these questions to explain Python object memory, profiling, and practical performance trade-offs in backend services.

## Memory Fundamentals

### 1. How does Python manage memory?
CPython primarily uses reference counting and supplements it with a cyclic garbage collector for reference cycles. Object lifetime and reclamation details are implementation-dependent, so avoid relying on immediate cleanup for external resources.

### 2. What is the difference between mutable and immutable objects?
Mutable objects can be changed in place; immutable objects cannot. Aliasing matters: two variables can refer to the same mutable object, so a mutation through one reference is visible through the other. Use copies or immutable data structures where isolation is required.

### 3. What causes memory leaks in a long-running Python service?
Common causes include unbounded caches, retained references in global collections, callbacks that keep objects alive, unclosed resources, and queues that grow faster than workers can process them. Compare memory over time under a repeatable workload and inspect object retention before assuming garbage collection is broken.

### 4. What are generators useful for?
Generators produce values lazily and can reduce peak memory when processing large streams. They do not make every operation faster, and a generator can still retain substantial memory if it closes over large objects or buffers data internally.

## Performance and Profiling

### 5. How do you investigate a slow Python endpoint?
1. Reproduce the workload and define a latency or throughput baseline.
2. Measure request-level latency and dependency timings.
3. Profile CPU time and inspect database queries, network waits, serialization, and lock contention.
4. Optimize the measured bottleneck, then rerun the same workload.
5. Add a regression test or benchmark when the behavior is stable enough to measure.

### 6. What is the difference between CPU-bound and I/O-bound work?
CPU-bound work spends most of its time executing computations. I/O-bound work spends substantial time waiting for external operations. AsyncIO or threads can improve I/O concurrency when dependencies support them; CPU-heavy work may need algorithmic improvements, native code, or process-based parallelism.

### 7. Does `__slots__` always improve performance?
No. `__slots__` can reduce per-instance memory for classes with many instances by avoiding a normal instance dictionary, but it restricts dynamic attributes and has inheritance and tooling implications. Measure before adopting it.

### 8. How do you reduce memory usage when processing large files?
Stream records instead of loading the entire file, use iterators and generators, bound batch sizes, release references when no longer needed, and avoid unnecessary copies. Consider backpressure so producers cannot create an unbounded backlog.

## Backend Scenarios

### 9. A service's memory rises throughout the day. What do you check?
- Compare memory, request volume, traffic mix, and deployment changes over time.
- Inspect cache size, queue depth, worker lifecycle, and retained object types.
- Reproduce the workload and take comparable memory snapshots.
- Confirm whether memory is live Python objects, allocator retention, or native-library usage.
- Apply limits and alerts, then validate that the fix prevents recurrence.

### 10. How do you communicate a performance improvement?
Report the baseline and changed measurement, workload and environment, sample size, latency percentiles or throughput, memory impact, and any trade-offs. Avoid claiming a universal speedup from a single local run.

## Key Takeaways

- Profile before optimizing.
- Distinguish CPU time, I/O wait, and database latency.
- Bound caches, queues, batches, and concurrency.
- Prefer streaming for large inputs and measure changes under repeatable conditions.
