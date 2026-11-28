# News Feed

A runnable, authenticated social news-feed MVP built with Flask and SQLite. It
supports user registration and profiles, follow/unfollow relationships,
and persistent post creation and retrieval.

## Architecture

- Flask exposes the REST API and validates request payloads.
- SQLite persists users, follow relationships, and posts with foreign-key
  constraints and indexes for relationship lookups and author timelines.
- Signed bearer tokens authenticate all user, follow, and post routes.
- Writes use explicit SQLite transactions; parameterized SQL is used for all
  user-controlled values.

See [`architecture.md`](architecture.md) for the schema, request flow, and
scaling limitations.

## Setup and run

From the repository root:

```bash
python -m pip install -r python/requirements.txt
python projects/news-feed/app.py
```

The API listens on `http://127.0.0.1:5002`. The default database is
`projects/news-feed/news_feed.sqlite3`. Set `NEWS_FEED_DATABASE` to change it
and set `NEWS_FEED_SECRET_KEY` to a strong secret outside local development.
The built-in development fallback secret is not suitable for deployment.

Check the process:

```bash
curl http://127.0.0.1:5002/health
```

## Demo flow

Register two users and log in:

```bash
curl -s http://127.0.0.1:5002/auth/register -H 'Content-Type: application/json'   -d '{"username":"alice","password":"correct-horse"}'
curl -s http://127.0.0.1:5002/auth/register -H 'Content-Type: application/json'   -d '{"username":"bob","password":"correct-horse"}'
curl -s http://127.0.0.1:5002/auth/login -H 'Content-Type: application/json'   -d '{"username":"alice","password":"correct-horse"}'
```

Set `TOKEN` to Alice's access token and `BOB_ID` to Bob's returned ID:

```bash
export TOKEN='<alice-access-token>'
export BOB_ID='<bob-user-id>'
curl -s "http://127.0.0.1:5002/users/$BOB_ID/follow" -X POST   -H "Authorization: Bearer $TOKEN"
curl -s http://127.0.0.1:5002/posts -X POST   -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json'   -d '{"body":"Hello from the news feed MVP"}'
```

## API contract

| Method | Endpoint | Behavior |
|---|---|---|
| POST | `/auth/register` | Create a user with a salted password hash |
| POST | `/auth/login` | Issue a signed, time-limited bearer token |
| GET | `/users` | List other users |
| GET | `/users/<user_id>` | Read profile and follow counts/status |
| PATCH | `/users/me` | Update the authenticated user's bio |
| POST | `/users/<user_id>/follow` | Follow a user; repeated requests are safe |
| DELETE | `/users/<user_id>/follow` | Unfollow a user |
| GET | `/users/<user_id>/followers` | List followers |
| GET | `/users/<user_id>/following` | List followed accounts |
| POST | `/posts` | Create a post as the authenticated user |
| GET | `/posts/<post_id>` | Retrieve a post |
| GET | `/health` | Process health check |

All user, follow, and post routes require a valid bearer token.
Users can only create posts as themselves; follow actions always use the
authenticated user as the follower. Posts are limited to 2,000 characters and
bios to 280 characters by default.

## Tests

Install dependencies, then run from the repository root:

```bash
python -m pytest projects/news-feed/tests -q
```

The integration suite covers authentication, persistence, profile validation,
follow/unfollow behavior, self-follow rejection, post creation and retrieval,
persistence across app instances, and invalid inputs.

## MVP scope and limitations

- Feed generation, cursor pagination, and ranking are not part of this
  milestone; the current API establishes the persistent social graph and post
  foundation for those capabilities.
- Edits, deletes, likes, comments, media, and search are out of scope.
- SQLite is appropriate for this local MVP. A larger deployment would need
  managed relational storage, schema migration tooling, caching, and a
  deliberate fan-out-on-read/write strategy.
- Tokens are signed and expire after one hour; there is no refresh-token or
  revocation mechanism in this MVP.
- The local Flask development server and fallback secret are not production
  deployment settings.
