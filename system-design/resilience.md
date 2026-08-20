# Resilience — Retries, Timeouts and Idempotency

## Overview

Resilience allows a backend system to continue behaving correctly when
dependencies fail, become slow, or return temporary errors.

The major concepts covered today are:

- Timeouts
- Retries
- Exponential backoff
- Idempotency
- Failure boundaries
- Retryable vs non-retryable errors

---

## 1. Timeouts

Every network call should have a reasonable timeout.

Without a timeout:

Client
  ↓
Service A
  ↓
Service B
  ↓
Service B hangs
  ↓
Service A waits indefinitely

Timeouts prevent resources from being held indefinitely.

---

## 2. Retries

Retries can help recover from transient failures.

Example:

Request
  ↓
Temporary failure
  ↓
Retry
  ↓
Success

Retries should generally be limited.

---

## 3. Exponential Backoff

Instead of retrying immediately every time:

Retry 1 → short delay
Retry 2 → longer delay
Retry 3 → even longer delay

This reduces pressure on an already struggling dependency.

---

## 4. Retryable Errors

Examples may include:

- Temporary network failure
- Connection reset
- Some 5xx responses
- Temporary service unavailability

Not every error should be retried.

---

## 5. Non-Retryable Errors

Examples:

- Invalid input
- Authentication failure
- Authorization failure
- Resource not found
- Validation failure

Retrying these usually does not solve the underlying problem.

---

## 6. Idempotency

An operation is idempotent when repeating the same logical request
does not create additional unintended side effects.

This is especially important for:

- Payments
- Order creation
- Booking
- Message submission
- Resource creation

---

## 7. Idempotency Key

A client can send:

Idempotency-Key: abc123

The server stores the result associated with that key.

If the same request arrives again with the same key,
the server can return the previous result instead of performing
the operation again.

---

## 8. Key Principle

Retries + non-idempotent operations can create duplicate side effects.

Therefore:

Retry
+
Idempotency
=
Safer distributed operations
