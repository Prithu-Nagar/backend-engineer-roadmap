# Chat Application — Architecture

## MVP boundary

The project is a runnable, single-process Flask chat application. It combines
an authenticated REST API, SQLite persistence, and room-scoped WebSockets.
The implementation prioritizes durable messages and authorization over
production-scale gateway infrastructure.

## Components

```text
                         +----------------------+
                         |        Client        |
                         +----------+-----------+
                                    |
                     +--------------+--------------+
                     |                             |
                 HTTPS/JSON                    WebSocket
                     |                             |
           +---------v----------+        +---------v----------+
           | Flask REST API     |        | Flask-Sock route   |
           | auth / rooms /     |        | room connection    |
           | message history    |        | lifecycle          |
           +---------+----------+        +---------+----------+
                     |                             |
                     +--------------+--------------+
                                    |
                           +--------v--------+
                           |     SQLite      |
                           | users / rooms / |
                           | members/messages|
                           +-----------------+

                  In-process room socket registry
                  broadcasts to connected clients
```

- **REST API** validates credentials, manages rooms and membership, persists
  messages, and serves chronological cursor-paginated history.
- **WebSocket route** authenticates the first frame, checks room membership,
  validates sends, persists before broadcasting, and removes closed sockets.
- **SQLite** stores users, rooms, memberships, and messages. A unique partial
  index enforces idempotency for `(room_id, sender_id, client_message_id)`.
- **Connection registry** tracks active sockets per room inside one process.

## Data and authorization model

- A user owns a room and is automatically its first member.
- Only the room owner can add existing users.
- Room membership is required to list room messages, send through REST, and
  connect/send through WebSocket.
- Passwords are stored as salted `scrypt` hashes.
- Access tokens are HMAC-signed and expire after one hour.
- Message history is queried by descending message ID and returned in
  chronological order within each page.
- Client-generated message IDs make REST and WebSocket retries idempotent per
  sender and room.

## Core flows

### Connect and authenticate

1. Client opens `/ws/rooms/<room_id>`.
2. The first JSON frame carries the bearer token; tokens are not placed in the
   URL.
3. The server verifies the signature, expiry, user, and room membership.
4. The socket is registered for that room and receives a `ready` event.

### Send and broadcast

1. Client sends a `send` event with a non-empty body and stable
   `client_message_id`.
2. The server validates the payload and rechecks current room membership.
3. A transaction finds an existing idempotent message or inserts a new row.
4. For a new message, the server broadcasts the persisted row to active room
   sockets. For a duplicate retry, it acknowledges only the retrying socket.
5. The sender and recipients receive the same event for a newly persisted
   message; existing recipients do not receive duplicate fan-out.

### Reconnect and catch up

1. Client reconnects and authenticates again.
2. Client requests `GET /rooms/<room_id>/messages` with the latest history
   cursor.
3. Client retries an unacknowledged send with the same client message ID.
4. The server resolves the retry to the original persisted message.

## Guarantees and limitations

**Implemented and covered by tests**

- Authenticated room membership and owner-only member addition.
- Durable SQLite message storage and paginated history.
- WebSocket authentication and authorization before joining a room.
- Membership revalidation before each WebSocket send.
- Persistence before live broadcast.
- Retry deduplication using a stable client message ID.
- Same-process broadcast to active room connections.

**Not implemented**

- Cross-process or cross-host fan-out; a shared broker/pub-sub layer is
  required for multiple workers.
- Bounded per-client queues or slow-consumer backpressure.
- Automatic history replay as part of the WebSocket handshake.
- Presence, read receipts, typing indicators, edits/deletes, and delivery
  acknowledgements.
- Production database migrations, deployment hardening, and operational
  observability.

The local SQLite database and in-process socket registry are deliberate MVP
choices. Do not describe this implementation as horizontally scalable or
production-ready.
