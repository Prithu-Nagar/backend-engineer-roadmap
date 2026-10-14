# SQL Transactions and Isolation — Interview Questions

Use these questions to explain transaction guarantees, concurrent updates, and consistency trade-offs in relational databases.

## Transaction Fundamentals

### 1. What are the ACID properties?
- **Atomicity:** a transaction succeeds as a unit or is rolled back.
- **Consistency:** committed changes preserve defined constraints and invariants.
- **Isolation:** concurrent transactions are controlled so their interactions follow the database's isolation semantics.
- **Durability:** committed changes survive failures within the database's durability guarantees.

### 2. What is the difference between `COMMIT` and `ROLLBACK`?
`COMMIT` makes the transaction's changes durable according to the database's guarantees. `ROLLBACK` discards uncommitted changes in the transaction. Applications should keep transaction boundaries narrow and handle exceptions without accidentally committing partial business operations.

### 3. What are common isolation levels?
- **Read Uncommitted:** may allow dirty reads where supported.
- **Read Committed:** prevents dirty reads; repeated reads may observe newer committed values.
- **Repeatable Read:** provides stronger guarantees for rows already read; exact phantom and snapshot behavior depends on the database.
- **Serializable:** aims to make concurrent execution equivalent to a serial order, potentially aborting transactions that must be retried.

Always explain the actual database implementation rather than assuming every engine implements each level identically.

### 4. Explain dirty reads, non-repeatable reads, and phantom reads.
A dirty read observes another transaction's uncommitted change. A non-repeatable read returns a different value for the same row on a later read. A phantom read occurs when repeating a predicate query returns a different set of rows due to concurrent changes.

## Concurrency and Correctness

### 5. How do lost updates happen?
Two transactions read the same value, independently calculate a new value, and overwrite each other's changes. Use an atomic SQL update, row locking, optimistic version checks, or an appropriate isolation strategy.

```sql
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = :product_id
  AND quantity > 0;
```

Check the affected-row count to determine whether stock was available.

### 6. How do you prevent overselling inventory?
Keep the availability check and decrement within one atomic database operation or transaction. Add constraints where appropriate, check affected rows, and define how the application handles conflicts or retries. A separate read followed by an unconditional update is vulnerable to races.

### 7. What is a deadlock and how should an application respond?
A deadlock occurs when transactions wait on resources held by each other. Databases generally detect and abort one participant. Keep transactions short, acquire locks in a consistent order, use suitable indexes, and retry the whole transaction when the error is recognized as retryable.

### 8. When would you use optimistic versus pessimistic locking?
Optimistic locking detects conflicts at write time, often through a version column, and is useful when conflicts are uncommon. Pessimistic locking acquires locks before changing data and can be useful for highly contended invariants, but may reduce throughput and increase deadlock risk.

## Interview Scenarios

### 9. A transfer debits one account but fails before crediting the other. What should happen?
Both changes should be part of one transaction so a failure rolls back the debit. External side effects such as notifications should occur after commit or through a reliable outbox/event pattern.

### 10. What should you consider when choosing an isolation level?
Identify the invariant that must be protected, the anomalies the application can tolerate, database-specific behavior, contention, retry requirements, and performance. Select the weakest level that safely preserves correctness, and test concurrency-sensitive flows.

## Key Takeaways

- Define the business invariant before selecting a locking strategy.
- Prefer atomic updates and database constraints for simple invariants.
- Keep transactions short and handle retryable conflicts deliberately.
- Test concurrent operations, not only sequential happy paths.
