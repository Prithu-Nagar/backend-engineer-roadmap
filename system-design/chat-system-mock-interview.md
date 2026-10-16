# Chat System — System Design Mock Interview

Practice explaining a one-to-one and group messaging system, including message delivery, history, presence, and failure recovery.

## 1. Clarify Requirements

Ask about concurrent users, peak messages per second, group size, message retention, ordering guarantees, offline delivery, read receipts, attachments, moderation, privacy, and geographic scope. Separate must-have requirements from later enhancements.

## 2. Define the API

Possible operations:
- `POST /conversations` — create a conversation.
- `GET /conversations` — list conversations for the authenticated user.
- `GET /conversations/{id}/messages?cursor=...` — fetch a page of history.
- `POST /conversations/{id}/messages` — send a message with a client-generated idempotency key.
- `POST /conversations/{id}/read-cursor` — advance the user's read position.

Authorize every operation against conversation membership. Validate payload size and content, rate-limit sends, and use stable error responses.

## 3. High-Level Architecture

1. API gateway or edge layer authenticates the connection.
2. Chat service validates membership and message input.
3. A relational database stores durable conversations, membership, and messages.
4. A transactional outbox records events with the message write.
5. A broker distributes message-created events to delivery workers.
6. WebSocket gateways deliver messages to connected clients.
7. Push notification workers notify offline users.
8. Cache stores short-lived presence and connection-routing information.

Keep durable message history separate from ephemeral presence state.

## 4. Message Send Flow

1. Client submits a message with an idempotency key.
2. Service authenticates the sender and verifies membership.
3. One database transaction inserts the message and outbox event.
4. The API acknowledges durable acceptance.
5. Outbox relay publishes the event; consumers may receive duplicates.
6. Delivery workers route the message to online sessions and schedule offline notifications.
7. Clients deduplicate by message ID and acknowledge delivery where required.

Explain the product meaning of “sent,” “delivered,” and “read”; they are different states.

## 5. Ordering, Duplicates, and Reconnection

- Define whether ordering is per conversation, per sender, or best-effort.
- Use a stable sequence or cursor for history and reconnect catch-up.
- Treat retries as at-least-once and make writes/delivery handlers idempotent.
- On reconnect, fetch missed messages from the last durable cursor; do not rely only on transient socket buffers.
- Avoid assuming wall-clock timestamps are a globally reliable ordering mechanism.

## 6. Scaling and Bottlenecks

- Partition message traffic by conversation or another key aligned with ordering.
- Use keyset pagination and a composite index for conversation history.
- Track hot group conversations and avoid fan-out work that blocks the send path.
- Apply backpressure to slow clients and cap queued outbound data.
- Scale WebSocket gateways separately from persistence and delivery workers.
- Define retention, archival, and deletion policies before choosing partitioning details.

## 7. Reliability and Security

Discuss multi-device sessions, reconnect storms, rate limits, spam/abuse controls, encryption requirements, key management, access logging, regional failure, backups, restore testing, and data deletion. Never log message bodies or credentials by default.

## 8. Observability

Measure send acknowledgement latency, delivery delay, failed deliveries, queue age/depth, reconnect rate, active connections, database saturation, and push notification failures. Trace message IDs across the write/outbox/consumer path without exposing private content.

## 9. Trade-Offs to Explain

- Relational database first versus a specialized distributed store.
- Polling versus WebSockets.
- Fan-out on write versus fan-out on read for large groups.
- Stronger ordering versus throughput.
- Synchronous delivery versus durable asynchronous delivery.

## Interview Wrap-Up

Summarize the core path, the durability boundary, duplicate handling, reconnect behavior, primary bottleneck, and the first two metrics you would alert on. State assumptions explicitly rather than inventing scale estimates.
