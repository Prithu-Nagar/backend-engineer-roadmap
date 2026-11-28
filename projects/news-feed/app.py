"""Authenticated social news-feed MVP backed by SQLite."""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import sqlite3
import time
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Any

from flask import Flask, g, jsonify, request

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_salt BLOB NOT NULL,
    password_hash BLOB NOT NULL,
    bio TEXT NOT NULL DEFAULT '',
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS follows (
    follower_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    followed_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    CHECK (follower_id <> followed_id)
);
CREATE INDEX IF NOT EXISTS ix_follows_followed ON follows(followed_id, follower_id);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_posts_author_id_id ON posts(author_id, id DESC);
"""


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    salt = salt or os.urandom(16)
    return salt, hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def _make_token(user_id: int, secret: str) -> str:
    payload = _b64(json.dumps(
        {"sub": user_id, "exp": int(time.time()) + 3600}, separators=(",", ":")
    ).encode())
    signature = _b64(hmac.new(secret.encode(), payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{signature}"


def _read_token(token: str, secret: str) -> int | None:
    try:
        payload, signature = token.split(".", 1)
        expected = _b64(hmac.new(secret.encode(), payload.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected):
            return None
        claims = json.loads(_unb64(payload))
        if int(claims["exp"]) <= int(time.time()):
            return None
        return int(claims["sub"])
    except (ValueError, TypeError, KeyError, json.JSONDecodeError, binascii.Error):
        return None


def create_app(config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("NEWS_FEED_DATABASE", str(Path(__file__).with_name("news_feed.sqlite3"))),
        SECRET_KEY=os.environ.get("NEWS_FEED_SECRET_KEY", "local-news-feed-secret-change-before-deployment"),
        MAX_POST_LENGTH=2000,
        MAX_BIO_LENGTH=280,
        MAX_PAGE_SIZE=100,
    )
    if config:
        app.config.update(config)

    def connect() -> sqlite3.Connection:
        connection = sqlite3.connect(app.config["DATABASE"], timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def database():
        connection = connect()
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def transaction():
        connection = connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    with database() as connection:
        connection.executescript(SCHEMA)

    def authenticated(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            scheme, _, token = request.headers.get("Authorization", "").partition(" ")
            user_id = (
                _read_token(token, app.config["SECRET_KEY"])
                if scheme.lower() == "bearer" else None
            )
            if user_id is None:
                return jsonify(error="unauthorized"), 401
            with database() as connection:
                user = connection.execute(
                    "SELECT id, username, bio FROM users WHERE id = ?", (user_id,)
                ).fetchone()
            if user is None:
                return jsonify(error="unauthorized"), 401
            g.user = user
            return function(*args, **kwargs)
        return wrapped

    @app.post("/auth/register")
    def register():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="invalid_json"), 400
        username, password = data.get("username"), data.get("password")
        if not isinstance(username, str) or not 3 <= len(username.strip()) <= 40:
            return jsonify(error="invalid_username"), 400
        if not isinstance(password, str) or len(password) < 8:
            return jsonify(error="invalid_password"), 400
        salt, password_hash = _hash_password(password)
        try:
            with transaction() as connection:
                cursor = connection.execute(
                    """INSERT INTO users(username, password_salt, password_hash, created_at)
                       VALUES (?, ?, ?, ?)""",
                    (username.strip(), salt, password_hash, int(time.time())),
                )
                user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            return jsonify(error="username_unavailable"), 409
        return jsonify(id=user_id, username=username.strip()), 201

    @app.post("/auth/login")
    def login():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("username"), str) or not isinstance(data.get("password"), str):
            return jsonify(error="invalid_credentials"), 400
        with database() as connection:
            user = connection.execute(
                """SELECT id, password_salt, password_hash FROM users
                   WHERE username = ? COLLATE NOCASE""",
                (data["username"].strip(),),
            ).fetchone()
        if user is None:
            return jsonify(error="invalid_credentials"), 401
        _, candidate = _hash_password(data["password"], user["password_salt"])
        if not hmac.compare_digest(candidate, user["password_hash"]):
            return jsonify(error="invalid_credentials"), 401
        return jsonify(
            access_token=_make_token(user["id"], app.config["SECRET_KEY"]),
            token_type="Bearer",
        ), 200

    @app.get("/users")
    @authenticated
    def list_users():
        with database() as connection:
            rows = connection.execute(
                """SELECT id, username, bio FROM users
                   WHERE id <> ? ORDER BY username COLLATE NOCASE, id""",
                (g.user["id"],),
            ).fetchall()
        return jsonify(users=[dict(row) for row in rows]), 200

    @app.get("/users/<int:user_id>")
    @authenticated
    def get_user(user_id: int):
        with database() as connection:
            row = connection.execute(
                "SELECT id, username, bio FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row is None:
                return jsonify(error="user_not_found"), 404
            counts = connection.execute(
                """SELECT
                    (SELECT COUNT(*) FROM follows WHERE followed_id = ?) AS followers_count,
                    (SELECT COUNT(*) FROM follows WHERE follower_id = ?) AS following_count""",
                (user_id, user_id),
            ).fetchone()
            is_following = connection.execute(
                "SELECT 1 FROM follows WHERE follower_id = ? AND followed_id = ?",
                (g.user["id"], user_id),
            ).fetchone() is not None
        return jsonify(
            **dict(row), followers_count=counts["followers_count"],
            following_count=counts["following_count"], is_following=is_following,
        ), 200

    @app.patch("/users/me")
    @authenticated
    def update_profile():
        data = request.get_json(silent=True)
        bio = data.get("bio") if isinstance(data, dict) else None
        if not isinstance(bio, str) or len(bio.strip()) > app.config["MAX_BIO_LENGTH"]:
            return jsonify(error="invalid_bio"), 400
        with transaction() as connection:
            connection.execute("UPDATE users SET bio = ? WHERE id = ?", (bio.strip(), g.user["id"]))
        return jsonify(id=g.user["id"], username=g.user["username"], bio=bio.strip()), 200

    @app.post("/users/<int:user_id>/follow")
    @authenticated
    def follow_user(user_id: int):
        if user_id == g.user["id"]:
            return jsonify(error="cannot_follow_self"), 400
        with transaction() as connection:
            if connection.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone() is None:
                return jsonify(error="user_not_found"), 404
            connection.execute(
                """INSERT OR IGNORE INTO follows(follower_id, followed_id, created_at)
                   VALUES (?, ?, ?)""",
                (g.user["id"], user_id, int(time.time())),
            )
        return jsonify(follower_id=g.user["id"], followed_id=user_id, following=True), 200

    @app.delete("/users/<int:user_id>/follow")
    @authenticated
    def unfollow_user(user_id: int):
        if user_id == g.user["id"]:
            return jsonify(error="cannot_follow_self"), 400
        with transaction() as connection:
            if connection.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone() is None:
                return jsonify(error="user_not_found"), 404
            connection.execute(
                "DELETE FROM follows WHERE follower_id = ? AND followed_id = ?",
                (g.user["id"], user_id),
            )
        return jsonify(follower_id=g.user["id"], followed_id=user_id, following=False), 200

    @app.get("/users/<int:user_id>/followers")
    @authenticated
    def list_followers(user_id: int):
        with database() as connection:
            if connection.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone() is None:
                return jsonify(error="user_not_found"), 404
            rows = connection.execute(
                """SELECT u.id, u.username FROM follows f JOIN users u ON u.id = f.follower_id
                   WHERE f.followed_id = ? ORDER BY u.id""", (user_id,)
            ).fetchall()
        return jsonify(users=[dict(row) for row in rows]), 200

    @app.get("/users/<int:user_id>/following")
    @authenticated
    def list_following(user_id: int):
        with database() as connection:
            if connection.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone() is None:
                return jsonify(error="user_not_found"), 404
            rows = connection.execute(
                """SELECT u.id, u.username FROM follows f JOIN users u ON u.id = f.followed_id
                   WHERE f.follower_id = ? ORDER BY u.id""", (user_id,)
            ).fetchall()
        return jsonify(users=[dict(row) for row in rows]), 200

    @app.post("/posts")
    @authenticated
    def create_post():
        data = request.get_json(silent=True)
        body = data.get("body") if isinstance(data, dict) else None
        if not isinstance(body, str) or not body.strip() or len(body.strip()) > app.config["MAX_POST_LENGTH"]:
            return jsonify(error="invalid_post"), 400
        with transaction() as connection:
            cursor = connection.execute(
                "INSERT INTO posts(author_id, body, created_at) VALUES (?, ?, ?)",
                (g.user["id"], body.strip(), int(time.time())),
            )
            post_id = cursor.lastrowid
            row = connection.execute(
                """SELECT p.id, p.author_id, u.username AS author_username, p.body, p.created_at
                   FROM posts p JOIN users u ON u.id = p.author_id WHERE p.id = ?""",
                (post_id,),
            ).fetchone()
        return jsonify(dict(row)), 201

    @app.get("/posts/<int:post_id>")
    @authenticated
    def get_post(post_id: int):
        with database() as connection:
            row = connection.execute(
                """SELECT p.id, p.author_id, u.username AS author_username, p.body, p.created_at
                   FROM posts p JOIN users u ON u.id = p.author_id WHERE p.id = ?""",
                (post_id,),
            ).fetchone()
        if row is None:
            return jsonify(error="post_not_found"), 404
        return jsonify(dict(row)), 200

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5002, debug=False)
