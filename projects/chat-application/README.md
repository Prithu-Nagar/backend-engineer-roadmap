# Chat Application

Day 68 architecture artifact for the Chat Application milestone.

The detailed project architecture is documented in:

- `architecture.md`

The design focuses on WebSocket connection ownership, durable message storage,
cross-instance fan-out, reconnect behavior, ordering, idempotency, and
backpressure.


## Runnable authenticated chat API — Day 25

The application provides authenticated room membership, SQLite-backed
messages, cursor-paginated history, and a Flask-Sock WebSocket endpoint for
live room messaging. Persistence, password hashing, and signed access tokens
use Python standard-library modules.

### Setup and run

Install the repository dependencies, then start the API from the repository
root:

```bash
python -m pip install -r python/requirements.txt
python projects/chat-application/app.py
```

The default SQLite database is `projects/chat-application/chat.sqlite3`.
Override it with `CHAT_DATABASE`; set `CHAT_SECRET_KEY` to a strong secret
outside local development.

### API flow

1. `POST /auth/register` with `{"username":"alice","password":"at-least-8-chars"}`.
2. `POST /auth/login` with the same credentials; send the returned token as
   `Authorization: Bearer <access_token>`.
3. `POST /rooms` with `{"name":"general"}`; the creator becomes the owner
   and first member.
4. The room owner adds an existing user with
   `POST /rooms/<room_id>/members` and `{"user_id":2}`.
5. Members send messages through `POST /rooms/<room_id>/messages` with
   `{"body":"Hello"}`.
6. Members retrieve history through
   `GET /rooms/<room_id>/messages?limit=50` and continue older pages with
   the returned `next_before_id` cursor.
7. Connect to `ws://localhost:5001/ws/rooms/<room_id>`. The first WebSocket
   frame must be `{"token":"<access_token>"}`. After a `ready` response, send
   `{"type":"send","client_message_id":"<stable-client-id>","body":"Hello"}`.
   The server broadcasts the persisted message as a `message` event to active
   connections in that room.

All room and message operations require a valid bearer token and current room
membership. Only the room owner can add members. WebSocket connections
authenticate before joining a room and membership is rechecked for each send.
Use a stable client-generated message ID when retrying after reconnect: the
same sender, room, and ID resolve to the original persisted message rather
than creating a duplicate. Message history remains the recovery path for
messages missed while disconnected.

### Tests

```bash
python -m pytest projects/chat-application/tests -q
```

### Scope and limitations

The WebSocket connection registry and live fan-out are in-process; they do
not deliver between multiple worker processes or hosts. Durable SQLite history
allows clients to recover missed messages after reconnect, while the
client-generated message ID makes retries idempotent. A shared broker and
production database are intentionally outside this MVP. Change the default
development secret before exposing the service.



## Real-time transport and reconnect behavior

- WebSocket route: `/ws/rooms/<room_id>`.
- Authentication is the first JSON frame; the access token is not placed in
  the URL or logged by the application.
- The server validates room membership at connection time and again before
  accepting each message.
- A message is committed to SQLite before it is broadcast to connected clients.
- `client_message_id` is unique per room and sender. Replaying the same ID
  returns the original message, making reconnect retries safe.
- The in-process socket registry is a single-process demo adapter, not
  cross-instance delivery. Clients use the REST history endpoint to catch up
  after disconnects.

Install dependencies and run the integration tests:

```bash
python -m pip install -r python/requirements.txt
python -m pytest projects/chat-application/tests -q
```
