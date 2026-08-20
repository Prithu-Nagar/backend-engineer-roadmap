# Rate Limiting

Rate limiting controls how many requests a client can make to a system within a defined period.

It protects backend systems from:

- Excessive traffic
- Abuse
- Accidental request spikes
- Denial-of-service attempts
- Resource exhaustion

---

## Why Do We Need Rate Limiting?

Without rate limiting, a single client could send a very large number of requests and consume shared system resources.

Example:

Client
   |
   | 10,000 requests
   ↓
API
   |
   ↓
Database

This can result in:

High CPU usage
High memory usage
Database overload
Increased latency
Service instability

With rate limiting:

Client
   |
   | Requests
   ↓
Rate Limiter
   |
   ├── Allowed → Backend
   |
   └── Rejected → 429
Basic Rate Limiting Model

A rate limit can be expressed as:

100 requests / minute

This means that a client is allowed to make at most 100 requests during the defined time period.

A system can apply limits based on:

IP address
User ID
API key
Access token
Client application
Endpoint
HTTP 429

When a client exceeds its allowed request rate, the server can return:

429 Too Many Requests

The response can also provide information about when the client can retry.

Example:

HTTP/1.1 429 Too Many Requests
Retry-After: 30
Common Rate Limiting Algorithms
1. Fixed Window

The fixed-window algorithm divides time into fixed intervals.

Example:

Limit: 100 requests / minute

12:00:00 ───────── 12:00:59
          100 requests

12:01:00 ───────── 12:01:59
          100 requests

Each client gets a new request allowance when the window changes.

Advantages
Simple
Easy to implement
Low memory usage
Disadvantages

Requests can cluster around a window boundary.

Example:

12:00:50 → 100 requests
12:01:00 → 100 requests

The system may receive 200 requests within a very short period even though the configured limit is 100 requests per minute.

2. Sliding Window

A sliding-window algorithm considers a continuously moving time interval.

For example:

Last 60 seconds

Instead of resetting at a fixed clock boundary, the system checks requests within the previous 60 seconds.

Advantages
More accurate than fixed windows
Reduces boundary spikes
Disadvantages
More state may be required
More computationally expensive
3. Token Bucket

The token bucket algorithm maintains a bucket containing tokens.

Each request consumes a token.

        Tokens
      ┌─────────┐
      │ ● ● ● ● │
      │ ● ● ●   │
      └────┬────┘
           │
           ↓
        Request
           │
           ↓
       Consume 1

Tokens are added to the bucket at a configured rate.

If tokens are available:

Request
   ↓
Token available
   ↓
Consume token
   ↓
Allow request

If no tokens are available:

Request
   ↓
No token
   ↓
Reject
   ↓
429

The bucket has a maximum capacity, which allows controlled bursts.

4. Leaky Bucket

The leaky-bucket algorithm processes requests at a controlled rate.

Conceptually:

Incoming Requests
       ↓
   ┌─────────┐
   │  Queue  │
   └────┬────┘
        ↓
  Fixed Processing Rate
        ↓
     Backend

Requests accumulate in a queue and are processed at a controlled rate.

Advantages
Smooths traffic
Controls processing rate
Disadvantages
Queues can grow
Requests may experience additional latency
Excess requests may need to be rejected
Token Bucket vs Leaky Bucket
Feature	Token Bucket	Leaky Bucket
Allows bursts	Yes	Limited
Controls average rate	Yes	Yes
Queue required	No	Usually
Common use	APIs	Traffic shaping
Burst handling	Flexible	More controlled
Distributed Rate Limiting

In a distributed backend, multiple application servers may receive requests.

                    ┌─── Service 1
                    │
Client → Gateway ───┼─── Service 2
                    │
                    └─── Service 3

If each server maintains its own rate-limit counter, the limit may not be globally accurate.

Example:

Limit = 100 requests/minute

Server 1 → 100
Server 2 → 100
Server 3 → 100

The client could effectively make 300 requests.

---

## Practical Example

A typical API gateway may enforce a rule such as:

- 100 requests per minute per user
- 10 requests per second per IP address
- 500 requests per minute across a shared service

A Redis-backed counter is often used in distributed systems so each request can be checked against a shared rate-limit state.

Example flow:

Client request
   |
   v
API gateway
   |
   v
Check rate-limit key in Redis
   |
   +-- within limit --> forward request
   |
   +-- over limit ----> 429 Too Many Requests

This allows consistent enforcement even when multiple application instances are serving traffic.

Centralized Rate Limiting

A shared store can maintain rate-limit state.

A common architecture is:

Client
   ↓
API Gateway
   ↓
Rate Limiter
   ↓
Redis
   ↓
Backend Services

Redis can store:

Request counters
Token counts
Expiration information
Per-user limits
Per-IP limits

This allows multiple application servers to share the same rate-limit state.

Rate Limiting at the API Gateway

Rate limiting is commonly implemented at an API Gateway.

Client
   ↓
API Gateway
   ↓
Rate Limiter
   ↓
Authentication
   ↓
Backend Services

The gateway can reject excessive requests before they reach application services.

This reduces unnecessary load on:

Application servers
Databases
Internal services
Different Rate Limits

Different endpoints may require different limits.

Example:

GET /tasks
100 requests/minute

POST /tasks
30 requests/minute

POST /login
5 requests/minute

POST /password-reset
3 requests/minute

Authentication-related endpoints often require stricter limits because they can be targeted for abuse.

Rate Limiting by User

Authenticated users can be limited using their user ID.

Example:

user:123
100 requests/minute

The rate limiter maintains a separate state for each user.

Rate Limiting by IP

Unauthenticated traffic can be limited using an IP address.

Example:

192.168.1.10
60 requests/minute

However, IP-based limiting should be designed carefully because multiple legitimate users can sometimes share the same public IP.

Rate Limiting by API Key

For APIs used by external clients, an API key can be used as the rate-limit identity.

Example:

API Key A → 1,000 requests/hour
API Key B → 10,000 requests/hour

This allows different clients or subscription levels to receive different limits.

Rate Limiting Architecture

A production-style architecture can look like:

                     ┌──────────────┐
                     │    Client    │
                     └──────┬───────┘
                            ↓
                     ┌──────────────┐
                     │ API Gateway  │
                     └──────┬───────┘
                            ↓
                     ┌──────────────┐
                     │Rate Limiter  │
                     └──────┬───────┘
                            ↓
                     ┌──────────────┐
                     │    Redis     │
                     └──────┬───────┘
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
             Backend 1           Backend 2
Important Design Considerations

When designing a rate limiter, consider:

Identity

What defines a client?

IP
User
API key
Token
Limit

How many requests are allowed?

100 requests/minute
Window

What time period is used?

second
minute
hour
day
Burst Handling

Should short bursts of requests be allowed?

Storage

Where is rate-limit state stored?

Memory
Redis
Distributed cache
Response

What happens when the limit is exceeded?

Usually:

429 Too Many Requests
Common Mistakes
1. Limiting only individual servers

This can produce incorrect limits in a distributed system.

2. Ignoring burst traffic

A fixed-window implementation can allow unexpected traffic spikes around boundaries.

3. Using only IP-based limits

This can unfairly affect multiple users sharing an IP address.

4. Applying the same limit everywhere

Different endpoints often have different resource costs and security requirements.

5. Running rate limiting after expensive processing

The rate limiter should reject excessive requests as early as practical.

Interview Questions
What is rate limiting?

Rate limiting restricts how frequently a client can access a service during a defined period.

Why is rate limiting needed?

To protect services from abuse, traffic spikes, resource exhaustion, and excessive requests.

What is HTTP 429?

429 Too Many Requests indicates that the client has exceeded the server's request rate limit.

What is a token bucket?

A rate-limiting algorithm where tokens are generated at a defined rate and requests consume tokens.

Why use Redis for distributed rate limiting?

Redis provides a shared, fast data store that multiple application servers can use to maintain consistent rate-limit state.

Where should rate limiting be implemented?

For many architectures, implementing it at the API Gateway provides an efficient early protection layer before traffic reaches backend services.

Revision Summary
Client
   ↓
API Gateway
   ↓
Rate Limiter
   ↓
Check Limit
   ├── Allowed → Backend
   │
   └── Exceeded → 429

Key concepts:

Fixed Window
Sliding Window
Token Bucket
Leaky Bucket
Distributed Rate Limiting
Redis
API Gateway
HTTP 429
Burst Handling
Per-user and per-IP limits
API-key-based limits
