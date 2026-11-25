# Chat Application

Day 68 architecture artifact for the Chat Application milestone.

The detailed project architecture is documented in:

- `architecture.md`

The design focuses on WebSocket connection ownership, durable message storage,
cross-instance fan-out, reconnect behavior, ordering, idempotency, and
backpressure.


## Runnable authenticated chat API — Day 25

The first implementation increment provides authenticated room membership,
SQLite-backed messages, and cursor-paginated message history. It uses Flask
and only Python standard-library modules for persistence, password hashing,
and signed access tokens.

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

All room and message operations require a valid bearer token and current room
membership. Only the room owner can add members. Message history is returned
in chronological order within each page; IDs provide a stable cursor.

### Tests

```bash
python -m pytest projects/chat-application/tests -q
```

### Scope and limitations

This is the Day 25 persistence and authorization increment. Messages are
persisted before the API returns success, but the transport is HTTP polling;
WebSocket real-time send/receive, reconnect fan-out, cross-instance pub/sub,
message idempotency, and production database deployment remain out of scope
for this day. SQLite and the local signed-token setup are a runnable MVP, not
a production deployment recipe. Change the default development secret before
exposing the service.
