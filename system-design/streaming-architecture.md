# Streaming Architecture

Day 52 focuses on delivering backend and AI responses incrementally instead of
waiting for the complete result before sending anything to the client.

## Why Streaming?

Streaming can reduce perceived latency for long-running responses and lets a
client render partial progress while the producer is still working.

Common examples:

- LLM token streaming
- Large report generation
- Progress updates
- Server-Sent Events (SSE)
- Log or event feeds

## High-Level Flow

```text
Client
  ↓
API / Gateway
  ↓
Application Service
  ↓
Producer / LLM / Worker
  ↓
Incremental Chunks
  ↓
Streaming Response
  ↓
Client Renderer
```

The producer should emit bounded chunks rather than accumulating the entire
response in application memory.

## HTTP Streaming Options

| Approach | Typical use | Connection model |
|---|---|---|
| Chunked HTTP response | Incremental text/data | One HTTP response |
| SSE | Server-to-client events | Long-lived HTTP |
| WebSocket | Bidirectional real-time interaction | Persistent socket |

For one-way incremental AI output, SSE or a streamed HTTP response can be
simpler than introducing a bidirectional protocol.

## Backpressure

A producer can generate data faster than the client can consume it. A streaming
service should therefore consider:

- Bounded buffers
- Cancellation when the client disconnects
- Producer rate limits
- Chunk sizing
- Queue depth
- Timeouts

The goal is to avoid unbounded memory growth while preserving useful throughput.

## Failure Handling

Streaming changes failure semantics because a response may already be partially
visible to the client.

Design for:

1. Clear start and completion events where appropriate.
2. A structured terminal error event for protocols such as SSE.
3. Cancellation when the client disconnects.
4. Idempotent work where a client may retry after an interrupted stream.
5. Metrics for time-to-first-byte, time-to-first-token, total duration, and
   disconnected streams.

## LLM Streaming

```text
User Request
    ↓
API Service
    ↓
LLM Client
    ↓
Token / Chunk Stream
    ↓
Validation / Safety Boundary
    ↓
SSE or HTTP Stream
    ↓
Browser / Client
```

The backend should keep authentication, authorization, rate limiting, logging,
and cost controls outside the model provider boundary.

## Scaling Considerations

Long-lived streaming connections consume connection and worker resources.
Production designs should consider:

- Async I/O for connection handling
- Load-balancer idle timeouts
- Connection limits
- Horizontal scaling
- Shared state only when required
- Queue-based producers for expensive background work
- Observability per stream

## Interview Checklist

- When would you use SSE instead of WebSockets?
- How do you handle client disconnects?
- What is backpressure?
- How do you measure time-to-first-token?
- How do load balancers affect long-lived streams?
- How do you retry an interrupted stream safely?
