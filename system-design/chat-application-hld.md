# HLD — Chat Application

## 1. Problem Statement

Design a chat application that supports direct and group conversations, near
real-time message delivery, durable message history, reconnects, and horizontal
scaling.

The design separates the real-time connection path from durable storage so a
WebSocket connection is not treated as the source of truth for message history.

## 2. Functional Requirements

- Create direct and group conversations.
- Add and remove group members.
- Establish authenticated WebSocket connections.
- Send and receive messages in near real time.
- Persist messages durably.
- Fetch message history with cursor-based pagination.
- Track a user's read position.
- Reconnect after temporary network failures.
- Deliver messages to currently connected recipients.
- Preserve messages when a recipient is temporarily offline.

## 3. Non-Functional Requirements

- Low latency for online message delivery.
- Durable message history.
- Horizontal scaling across application instances.
- Per-user and per-room authorization.
- Idempotent client retries.
- Backpressure when clients or downstream systems are slow.
- Observable connection, delivery, and persistence failures.

## 4. High-Level Architecture

```text
                    +-------------------+
                    |   Mobile / Web    |
                    +---------+---------+
                              |
                    HTTPS / WebSocket
                              |
                    +---------v---------+
                    | Load Balancer /   |
                    | WebSocket Gateway |
                    +---------+---------+
                              |
                +-------------+-------------+
                |                           |
        +-------v--------+          +-------v--------+
        | Chat API       |          | Connection     |
        | Auth / Rooms   |          | Gateway        |
        +-------+--------+          +-------+--------+
                |                           |
                |                           |
        +-------v--------+          +-------v--------+
        | PostgreSQL     |          | Pub/Sub /      |
        | rooms/messages |          | Broker         |
        +----------------+          +-------+--------+
                                            |
                                  +---------v---------+
                                  | Connected gateway |
                                  | instances         |
                                  +-------------------+

                    Offline/history path
                              |
                    +---------v---------+
                    | PostgreSQL /      |
                    | durable storage   |
                    +-------------------+
```

The exact broker can vary. Redis Pub/Sub can work for transient fan-out, while a
durable broker is preferable when downstream processing or replay is required.

## 5. Message Flow

1. The client authenticates and opens a WebSocket connection.
2. The gateway validates the user's room membership.
3. The client sends a message with a client-generated idempotency identifier.
4. The chat service validates authorization and message size.
5. The message is persisted before it is treated as durable.
6. A fan-out event is published for currently connected recipients.
7. Gateway instances deliver the message to local connections.
8. Offline recipients read the persisted history after reconnecting.
9. The client advances its read cursor after successfully processing messages.

The persistence boundary should be explicit. A successful WebSocket write alone
must not imply that the message is durably stored.

## 6. Data Model

Core entities:

- `chat_users`
- `chat_rooms`
- `room_members`
- `chat_messages`

The `room_members` row owns membership and the user's read cursor. The
`chat_messages` table owns immutable message identity plus edit/delete metadata.

The Day 68 SQL exercise uses `(created_at, message_id)` as a deterministic cursor
for history pagination.

## 7. WebSocket Scaling

A single WebSocket connection is stateful at the connection layer, but the
overall service should remain horizontally scalable.

Important boundaries:

- The load balancer routes the initial upgrade request.
- A gateway instance owns the live socket after the upgrade.
- Shared room membership and message state live outside the gateway process.
- Cross-instance fan-out uses a shared pub/sub or broker layer.
- Connection registries are local to each gateway instance.
- Reconnects may land on a different instance without losing durable history.

Sticky sessions can reduce connection churn in some deployments, but they should
not be required for correctness.

## 8. Ordering and Delivery Semantics

Per-room ordering is more important than global ordering.

A practical design:

- Assign a monotonic message identifier within the durable store.
- Use the persisted message identifier as the client-visible ordering cursor.
- Treat delivery as at-least-once.
- Deduplicate using `client_message_id` and message identifiers.
- Accept that a client may receive a duplicate after reconnect or retry.

Exactly-once end-to-end delivery is usually not a useful assumption for a
distributed WebSocket system.

## 9. Offline Users and Read State

Messages remain in durable storage even when no WebSocket is active.

On reconnect:

1. Authenticate the user.
2. Revalidate room membership.
3. Resume from the client's last known message cursor.
4. Fetch missed messages from durable storage.
5. Rejoin live fan-out.
6. Advance the read cursor after the client confirms processing.

This avoids making broker retention or gateway memory the only source of missed
messages.

## 10. Backpressure and Failure Handling

Potential failures include:

- Slow WebSocket clients.
- Disconnected clients during fan-out.
- Gateway process failure.
- Broker unavailability.
- Database latency.
- Duplicate client retries.
- Hot rooms with very high fan-out.

Controls include:

- Per-connection outbound queues with bounded capacity.
- Timeouts around network writes.
- Disconnecting persistently slow consumers.
- Rate limits on message creation.
- Retry policies for transient persistence/broker failures.
- Idempotency keys for client retries.
- Metrics for queue depth and delivery latency.
- Dead-letter or retry handling for asynchronous downstream work.

A gateway should not allow one slow client to block delivery to an entire room.

## 11. Capacity Considerations

Illustrative assumptions should be replaced with measured workload data.

For a design review, estimate:

- Concurrent WebSocket connections.
- Messages per second at average and peak.
- Average message size.
- Average room size.
- Fan-out multiplier.
- Message retention period.
- Read-history QPS.
- Reconnect rate during deployments or regional failures.

The dominant scaling dimension may be connection count, message fan-out, storage
write rate, or history reads depending on workload.

## 12. Security

- Authenticate WebSocket upgrades.
- Authorize room membership on connect and message send.
- Validate message length and content boundaries.
- Rate-limit abusive senders.
- Avoid trusting client-provided sender identity.
- Use TLS for WebSocket traffic.
- Protect administrative and moderation operations separately.
- Log security-relevant events without storing unnecessary message content.

## 13. Observability

Track:

- Active WebSocket connections.
- Connection and reconnect rates.
- Authentication failures.
- Messages accepted per second.
- Persistence latency and errors.
- Broker publish/consume latency.
- Fan-out latency.
- Per-connection queue depth.
- Dropped/disconnected slow consumers.
- History-query latency.
- End-to-end delivery latency.

Tracing should correlate the client message identifier with persistence and
fan-out operations without exposing sensitive message bodies.

## 14. Trade-offs

| Decision | Option A | Option B | Recommended starting point |
| --- | --- | --- | --- |
| Fan-out | Redis Pub/Sub | Durable broker | Pub/Sub for transient live delivery |
| History | SQL | NoSQL | PostgreSQL while relational access is sufficient |
| Ordering | Global | Per room | Per-room ordering |
| Delivery | At-most-once | At-least-once | At-least-once + deduplication |
| Sessions | Sticky | Reconnect anywhere | Reconnect anywhere |
| Pagination | Offset | Cursor | Cursor |
| Presence | Strong global state | Best effort | Best effort unless product requires stronger semantics |

## 15. Interview Explanation Sequence

1. Clarify direct versus group chat and message durability.
2. Define WebSocket and HTTP responsibilities.
3. Draw the gateway, persistence, and fan-out boundaries.
4. Explain cross-instance message delivery.
5. Explain ordering, retries, and idempotency.
6. Estimate connections, messages, storage, and fan-out.
7. Discuss slow consumers and gateway failure.
8. Close with security, observability, and trade-offs.
