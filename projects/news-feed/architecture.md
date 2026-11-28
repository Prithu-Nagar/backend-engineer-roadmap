# News Feed Architecture

## Components

- **API layer:** Flask routes handle authentication, profile, follow, and post
  requests.
- **Authentication:** HMAC-signed bearer tokens identify the caller. Passwords
  are stored as salted scrypt hashes.
- **Persistence:** SQLite stores users, directed follow edges, and posts.
  Foreign keys cascade when a user is removed.

## Data model

```text
users
  id (PK)
  username (UNIQUE, case-insensitive)
  password_salt
  password_hash
  bio
  created_at

follows
  follower_id (PK, FK -> users.id)
  followed_id (PK, FK -> users.id)
  created_at
  CHECK follower_id != followed_id

posts
  id (PK)
  author_id (FK -> users.id)
  body
  created_at
```

The composite primary key on `follows` prevents duplicate edges. An additional
index on `(followed_id, follower_id)` supports follower lookups. Posts have an
index on `(author_id, id DESC)` for author timelines.

## Request flows

1. Registration validates the username/password and persists a salted password
   hash.
2. Login verifies the password and returns a signed, one-hour bearer token.
3. Follow/unfollow operations use the authenticated user as `follower_id`;
   clients cannot nominate another follower.
4. Post creation derives `author_id` from the authenticated identity.
5. Post retrieval returns the selected post to an authenticated user.

## Current milestone boundary

This milestone establishes persistent users, directed follow relationships,
profiles, and authenticated post creation/retrieval. Feed assembly, cursor
pagination, and ranking are intentionally deferred to the next milestone.

## Consistency and security

- Each mutation runs in an explicit transaction.
- Foreign keys and uniqueness constraints enforce relationship integrity.
- SQL parameters are bound rather than interpolated.
- All social graph and content endpoints require authentication.
- Users cannot follow themselves or create content on behalf of another user.

## Limitations

This is a single-process Flask/SQLite MVP. It does not implement feed assembly, cursor
pagination, ranking, likes,
comments, media uploads, notifications, content moderation, block lists,
search, engagement ranking, token revocation, or distributed caching.
