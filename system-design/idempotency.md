# Idempotency

Idempotency means that performing the same operation multiple times
produces the same intended final result as performing it once.

Idempotency is especially important in distributed backend systems
where clients may retry requests because of:

- Network failures
- Timeouts
- Connection failures
- Client retries
- Load balancer retries
- Message redelivery

---

## The Duplicate Request Problem

Consider:

Client
  |
  | POST /payments
  |
  v
Payment Service
  |
  | Payment succeeds
  |
  v
Network failure

The client does not receive the response.

The client may retry:

Client
  |
  | POST /payments
  |
  v
Payment Service

Without duplicate-request protection, the payment could be processed twice.

Idempotency Key

The client sends a unique idempotency key:

POST /payments
Idempotency-Key: 8f5c2b7a-1234-4567

The server stores the result associated with the key.

Example:

idempotency_key
-------------------------
8f5c2b7a-1234-4567

status
-------------------------
COMPLETED

response
-------------------------
Payment ID: 501

When the same request arrives again:

Same Idempotency-Key
        |
        v
Check stored result
        |
```text
        +---- Found ----> Return previous response
```
        |
```text
        +---- Not found -> Process request
```
Basic Flow
Client
   |
   | Request + Idempotency-Key
   v
API Gateway / Backend
   |
   v
Idempotency Store
   |
```text
   +---- Key exists ----> Return stored result
```
   |
   +---- Key missing
            |
            v
      Process operation
            |
            v
      Store result
            |
            v
      Return response
Where to Store Idempotency Keys

Possible storage options:

Redis
PostgreSQL
DynamoDB
Other durable key-value stores

The choice depends on:

Required durability
Request volume
Latency requirements
TTL requirements
Consistency requirements
Idempotency Record

A typical record may contain:

key
user_id
request_hash
status
response_code
response_body
created_at
expires_at
Request Hash

An idempotency key should generally be associated with the
request it represents.

For example:

Idempotency-Key: abc123
Amount: 1000
Currency: INR

If the same key is reused with:

Amount: 5000

the server should not silently treat it as the original operation.

The request can be rejected because the key is associated with a
different request payload.

Idempotency States

A simple state model:

IN_PROGRESS
     |
     v
COMPLETED

Failure can result in:

IN_PROGRESS
     |
     v
FAILED

The exact retry behavior depends on whether the operation is safely
retryable.

Idempotency vs Retry

Retry answers:

Should we attempt the operation again?

Idempotency answers:

If the operation is attempted again, how do we prevent unintended
duplicate effects?

They work together.

Timeout
   |
   v
Retry
   |
   v
Idempotency check
   |
```text
   +---- Existing result -> Return previous result
```
   |
```text
   +---- New request -> Process safely
```
HTTP Methods and Idempotency

HTTP methods have different semantic expectations.

Generally:

GET is intended to be idempotent.
PUT is intended to be idempotent.
DELETE is intended to be idempotent.
POST is not inherently idempotent.

However, application-level idempotency can be added to POST operations.

This is especially useful for:

Payments
Orders
Account creation
Job submission
Resource creation
