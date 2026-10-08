-- Day 69: Feed / query design
-- PostgreSQL-oriented exercise for a read-heavy news-feed workload.

CREATE TABLE feed_users (
    user_id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE feed_follows (
    follower_id BIGINT NOT NULL REFERENCES feed_users(user_id) ON DELETE CASCADE,
    followee_id BIGINT NOT NULL REFERENCES feed_users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (follower_id, followee_id),
    CHECK (follower_id <> followee_id)
);

CREATE TABLE feed_posts (
    post_id BIGSERIAL PRIMARY KEY,
    author_id BIGINT NOT NULL REFERENCES feed_users(user_id),
    body TEXT NOT NULL CHECK (length(body) BETWEEN 1 AND 5000),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_feed_follows_follower_followee
    ON feed_follows (follower_id, followee_id);

CREATE INDEX idx_feed_posts_author_time
    ON feed_posts (author_id, created_at DESC, post_id DESC);

-- Fan-out-on-read query.
-- :viewer_id, :before_created_at, and :before_post_id are application params.
SELECT p.post_id, p.author_id, p.body, p.created_at
FROM feed_posts AS p
JOIN feed_follows AS f
  ON f.followee_id = p.author_id
WHERE f.follower_id = :viewer_id
  AND p.deleted_at IS NULL
  AND (
      :before_created_at IS NULL
      OR p.created_at < :before_created_at
      OR (
          p.created_at = :before_created_at
          AND p.post_id < :before_post_id
      )
  )
ORDER BY p.created_at DESC, p.post_id DESC
LIMIT 50;

-- Fetch a user's own recent posts without scanning unrelated authors.
SELECT post_id, body, created_at
FROM feed_posts
WHERE author_id = :author_id
  AND deleted_at IS NULL
ORDER BY created_at DESC, post_id DESC
LIMIT 50;

-- A materialized home-feed table can be used for high-read users when
-- fan-out-on-read becomes too expensive. The application can maintain a
-- bounded recent window per viewer and use a cursor over feed_item_id.
CREATE TABLE user_feed_items (
    viewer_id BIGINT NOT NULL REFERENCES feed_users(user_id) ON DELETE CASCADE,
    feed_item_id BIGSERIAL,
    post_id BIGINT NOT NULL REFERENCES feed_posts(post_id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES feed_users(user_id),
    inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (viewer_id, feed_item_id)
);

CREATE INDEX idx_user_feed_items_recent
    ON user_feed_items (viewer_id, feed_item_id DESC);

-- Cursor query for a materialized home feed.
SELECT feed_item_id, post_id, author_id, inserted_at
FROM user_feed_items
WHERE viewer_id = :viewer_id
  AND feed_item_id < :before_feed_item_id
ORDER BY feed_item_id DESC
LIMIT 50;

-- Production considerations:
-- 1. Measure follower/post distributions before choosing fan-out strategy.
-- 2. Avoid OFFSET for deep pagination; use stable cursors.
-- 3. Cache bounded feed pages with explicit invalidation/TTL policy.
-- 4. Consider a hybrid model: fan-out-on-write for normal accounts and
--    fan-out-on-read for very high-fan-out authors.
-- 5. Use EXPLAIN (ANALYZE, BUFFERS) on representative production-like data.
