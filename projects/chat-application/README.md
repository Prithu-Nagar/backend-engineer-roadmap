# Chat Application

A runnable, single-process chat MVP built with Flask, Flask-Sock, SQLite, and
signed bearer tokens. It supports authenticated room membership, durable
message history, live WebSocket delivery, and reconnect-safe message retries.

## Architecture

- Flask REST API handles registration, login, room creation, membership, and
  message history.
- SQLite is the source of truth for users, rooms, memberships, and messages.
- Flask-Sock provides room-scoped WebSocket connections.
- A process-local connection registry broadcasts persisted messages to active
  sockets in the same room.
- Clients recover messages missed while disconnected through the paginated
  history endpoint.

See [`architecture.md`](architecture.md) for component boundaries, request
flows, data model, guarantees, and scaling limitations.

## Setup and run

From the repository root:

```bash
python -m pip install -r python/requirements.txt
python projects/chat-application/app.py
```

The API listens on `http://127.0.0.1:5001`. The default database is
`projects/chat-application/chat.sqlite3`. Set `CHAT_DATABASE` to change it and
set `CHAT_SECRET_KEY` to a strong secret before use outside local development.
The development fallback secret is not suitable for deployment.

Check the process:

```bash
curl http://127.0.0.1:5001/health
```

## Demo flow

Run the API in one terminal. In another terminal, create two users and log in:

```bash
curl -s http://127.0.0.1:5001/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"correct-horse"}'

curl -s http://127.0.0.1:5001/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"bob","password":"correct-horse"}'

curl -s http://127.0.0.1:5001/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"correct-horse"}'
```

Use Alice's returned `access_token` as `TOKEN` below. Create a room and add
Bob using Bob's numeric user `id` returned by registration:

```bash
export TOKEN='<alice-access-token>'
export BOB_ID='<bob-user-id>'

curl -s http://127.0.0.1:5001/rooms \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"general"}'
```

Use the returned room `id` as `ROOM_ID`, then add Bob:

```bash
export ROOM_ID='<room-id>'
curl -s "http://127.0.0.1:5001/rooms/$ROOM_ID/members" \
  -X POST -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d "{\"user_id\":$BOB_ID}"
```

Send and read a message over the REST API:

```bash
curl -s "http://127.0.0.1:5001/rooms/$ROOM_ID/messages" \
  -X POST -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"body":"Hello from the chat MVP","client_message_id":"demo-message-1"}'

curl -s "http://127.0.0.1:5001/rooms/$ROOM_ID/messages" \
  -H "Authorization: Bearer $TOKEN"
```

For live messaging, connect a WebSocket client to
`ws://127.0.0.1:5001/ws/rooms/<room_id>`. Send the access token as the first
JSON frame: `{"token":"<access_token>"}`. After receiving `{"type":"ready"}`,
send `{"type":"send","body":"Hello live","client_message_id":"<stable-id>"}`.
The server emits a `message` event containing the persisted message to every
active socket in that room. Use the same stable ID when retrying after a
reconnect; the server acknowledges the original persisted message to the
retrying connection without broadcasting a second copy to the room.

## API contract

| Method | Endpoint | Behavior |
|---|---|---|
| POST | `/auth/register` | Create a user with a salted password hash |
| POST | `/auth/login` | Issue a signed, time-limited bearer token |
| POST | `/rooms` | Create a room; creator becomes owner and member |
| GET | `/rooms` | List rooms the authenticated user belongs to |
| POST | `/rooms/<room_id>/members` | Owner adds an existing user |
| POST | `/rooms/<room_id>/messages` | Persist a room message; optional idempotency key |
| GET | `/rooms/<room_id>/messages` | Read chronological history using `limit` and `before_id` |
| WebSocket | `/ws/rooms/<room_id>` | Authenticated live room send and broadcast |
| GET | `/health` | Process health check |

All room and message operations require a valid bearer token and current room
membership. Only the room owner can add members. Message bodies are limited to
4,000 characters by default; history page size is capped at 100.

## Tests

Install dependencies, then run from the repository root:

```bash
python -m pytest projects/chat-application/tests -q
```

The integration suite covers authentication, ownership and membership,
persistence across app instances, validation, cursor pagination, REST
idempotency, WebSocket authorization, live delivery, and reconnect
deduplication.

## Known limitations

- Live fan-out is process-local. Multiple workers or hosts require a shared
  broker/pub-sub layer; this MVP does not claim cross-instance delivery.
- A disconnected client catches up through the REST history endpoint; there
  is no automatic replay protocol on WebSocket reconnect.
- Slow-consumer backpressure, presence, read receipts, typing indicators,
  message edits/deletes, and delivery acknowledgements are out of scope.
- SQLite and the development server are for a local demonstration, not a
  production deployment. Production use needs managed secrets, TLS, a
  production database/migrations, operational monitoring, and a broker-backed
  gateway design.
