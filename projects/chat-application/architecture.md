# Chat Application — Architecture

## Day 68

Day 68 turns the Chat Application HLD into a project-oriented architecture
artifact that can be used for implementation planning and interview discussion.

## Architecture

```text
Client
  |
  +--> HTTPS --> Chat API ---------> PostgreSQL
  |
  +--> WebSocket --> Gateway ------> Local connections
                           |
                           v
                     Pub/Sub / Broker
                           |
                    Other gateway nodes
```

### Responsibilities

- **Chat API** owns room management, authentication, authorization, and durable
  message operations.
- **WebSocket Gateway** owns live connection lifecycle and local connection
  fan-out.
- **Pub/Sub or Broker** propagates live-message events between gateway instances.
- **PostgreSQL** stores users, rooms, memberships, messages, and read cursors.
- **Clients** reconnect and use durable cursors to recover missed messages.

## Core Flows

### Connect

1. Authenticate the user.
2. Upgrade the connection to WebSocket.
3. Validate requested room membership.
4. Register the connection with the local gateway.
5. Start bounded receive/send loops.

### Send Message

1. Validate the authenticated sender and room membership.
2. Validate the message body and client idempotency key.
3. Persist the message.
4. Publish a fan-out event.
5. Deliver the event to connected recipients.
6. Let offline users recover it from message history.

### Reconnect

1. Re-authenticate.
2. Revalidate room membership.
3. Send the client's last known message cursor.
4. Read missed messages from durable storage.
5. Rejoin live fan-out.

## Implementation Boundaries

The repository intentionally keeps Day 68 design work separate from the existing
Task Manager, Expense Tracker, URL Shortener, Rate Limiter, and Notification
Service implementations.

A future implementation can introduce a concrete WebSocket framework without
changing the core architectural boundaries documented here.

## Reliability Checklist

- [ ] WebSocket authentication is enforced.
- [ ] Room authorization is checked on connection and message send.
- [ ] Client retries use an idempotency key.
- [ ] Messages are durable before being acknowledged as persisted.
- [ ] Cross-instance fan-out is externalized.
- [ ] Slow consumers have bounded queues.
- [ ] Gateway failures can be recovered through reconnect.
- [ ] Message history uses cursor pagination.
- [ ] Delivery and persistence latency are observable.
