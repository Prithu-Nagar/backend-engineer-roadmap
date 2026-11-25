"""Authenticated chat REST API with SQLite-backed rooms and message history.

Real-time transport is intentionally left for the next project increment.
"""
from __future__ import annotations

import base64
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
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS room_members (
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at INTEGER NOT NULL,
    PRIMARY KEY (room_id, user_id)
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id),
    body TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_messages_room_id_id ON messages(room_id, id DESC);
"""


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    salt = salt or os.urandom(16)
    return salt, hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def _make_token(user_id: int, secret: str) -> str:
    payload = _b64(json.dumps({"sub": user_id, "exp": int(time.time()) + 3600},
                              separators=(",", ":")).encode())
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
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def create_app(config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("CHAT_DATABASE", str(Path(__file__).with_name("chat.sqlite3"))),
        SECRET_KEY=os.environ.get("CHAT_SECRET_KEY", "local-chat-secret-change-before-deployment"),
        MAX_MESSAGE_LENGTH=4000,
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
            user_id = _read_token(token, app.config["SECRET_KEY"]) if scheme.lower() == "bearer" else None
            if user_id is None:
                return jsonify(error="unauthorized"), 401
            with database() as connection:
                user = connection.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
            if user is None:
                return jsonify(error="unauthorized"), 401
            g.user = user
            return function(*args, **kwargs)
        return wrapped

    def is_member(connection: sqlite3.Connection, room_id: int, user_id: int) -> bool:
        return connection.execute(
            "SELECT 1 FROM room_members WHERE room_id = ? AND user_id = ?",
            (room_id, user_id),
        ).fetchone() is not None

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
                    "INSERT INTO users(username, password_salt, password_hash, created_at) VALUES (?, ?, ?, ?)",
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
                "SELECT id, username, password_salt, password_hash FROM users WHERE username = ? COLLATE NOCASE",
                (data["username"].strip(),),
            ).fetchone()
        if user is None:
            return jsonify(error="invalid_credentials"), 401
        _, candidate = _hash_password(data["password"], user["password_salt"])
        if not hmac.compare_digest(candidate, user["password_hash"]):
            return jsonify(error="invalid_credentials"), 401
        return jsonify(access_token=_make_token(user["id"], app.config["SECRET_KEY"]), token_type="Bearer"), 200

    @app.post("/rooms")
    @authenticated
    def create_room():
        data = request.get_json(silent=True)
        name = data.get("name") if isinstance(data, dict) else None
        if not isinstance(name, str) or not name.strip() or len(name.strip()) > 100:
            return jsonify(error="invalid_room_name"), 400
        now = int(time.time())
        with transaction() as connection:
            cursor = connection.execute(
                "INSERT INTO rooms(name, owner_id, created_at) VALUES (?, ?, ?)",
                (name.strip(), g.user["id"], now),
            )
            room_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO room_members(room_id, user_id, joined_at) VALUES (?, ?, ?)",
                (room_id, g.user["id"], now),
            )
        return jsonify(id=room_id, name=name.strip(), owner_id=g.user["id"]), 201

    @app.post("/rooms/<int:room_id>/members")
    @authenticated
    def add_member(room_id: int):
        data = request.get_json(silent=True)
        member_id = data.get("user_id") if isinstance(data, dict) else None
        if not isinstance(member_id, int) or isinstance(member_id, bool):
            return jsonify(error="invalid_user_id"), 400
        with transaction() as connection:
            room = connection.execute("SELECT owner_id FROM rooms WHERE id = ?", (room_id,)).fetchone()
            if room is None:
                return jsonify(error="room_not_found"), 404
            if room["owner_id"] != g.user["id"]:
                return jsonify(error="forbidden"), 403
            if connection.execute("SELECT 1 FROM users WHERE id = ?", (member_id,)).fetchone() is None:
                return jsonify(error="user_not_found"), 404
            connection.execute(
                "INSERT OR IGNORE INTO room_members(room_id, user_id, joined_at) VALUES (?, ?, ?)",
                (room_id, member_id, int(time.time())),
            )
        return jsonify(room_id=room_id, user_id=member_id, membership="active"), 200

    @app.get("/rooms")
    @authenticated
    def list_rooms():
        with database() as connection:
            rooms = connection.execute(
                """SELECT r.id, r.name, r.owner_id, r.created_at
                   FROM rooms r JOIN room_members m ON m.room_id = r.id
                   WHERE m.user_id = ? ORDER BY r.id""",
                (g.user["id"],),
            ).fetchall()
        return jsonify(rooms=[dict(row) for row in rooms]), 200

    @app.post("/rooms/<int:room_id>/messages")
    @authenticated
    def send_message(room_id: int):
        data = request.get_json(silent=True)
        body = data.get("body") if isinstance(data, dict) else None
        if not isinstance(body, str) or not body.strip() or len(body.strip()) > app.config["MAX_MESSAGE_LENGTH"]:
            return jsonify(error="invalid_message"), 400
        with transaction() as connection:
            if connection.execute("SELECT 1 FROM rooms WHERE id = ?", (room_id,)).fetchone() is None:
                return jsonify(error="room_not_found"), 404
            if not is_member(connection, room_id, g.user["id"]):
                return jsonify(error="forbidden"), 403
            cursor = connection.execute(
                "INSERT INTO messages(room_id, sender_id, body, created_at) VALUES (?, ?, ?, ?)",
                (room_id, g.user["id"], body.strip(), int(time.time())),
            )
            message_id = cursor.lastrowid
            row = connection.execute(
                """SELECT m.id, m.room_id, m.sender_id, u.username AS sender_username,
                          m.body, m.created_at
                   FROM messages m JOIN users u ON u.id = m.sender_id WHERE m.id = ?""",
                (message_id,),
            ).fetchone()
        return jsonify(dict(row)), 201

    @app.get("/rooms/<int:room_id>/messages")
    @authenticated
    def message_history(room_id: int):
        try:
            limit = int(request.args.get("limit", 50))
            before_id = int(request.args["before_id"]) if "before_id" in request.args else None
        except ValueError:
            return jsonify(error="invalid_pagination"), 400
        if not 1 <= limit <= app.config["MAX_PAGE_SIZE"] or (before_id is not None and before_id < 1):
            return jsonify(error="invalid_pagination"), 400
        with database() as connection:
            if connection.execute("SELECT 1 FROM rooms WHERE id = ?", (room_id,)).fetchone() is None:
                return jsonify(error="room_not_found"), 404
            if not is_member(connection, room_id, g.user["id"]):
                return jsonify(error="forbidden"), 403
            query = """SELECT m.id, m.room_id, m.sender_id, u.username AS sender_username,
                              m.body, m.created_at
                       FROM messages m JOIN users u ON u.id = m.sender_id
                       WHERE m.room_id = ?"""
            parameters: list[Any] = [room_id]
            if before_id is not None:
                query += " AND m.id < ?"
                parameters.append(before_id)
            query += " ORDER BY m.id DESC LIMIT ?"
            parameters.append(limit)
            rows = connection.execute(query, parameters).fetchall()
        # Return chronological order within the selected page.
        messages = [dict(row) for row in reversed(rows)]
        next_before_id = messages[0]["id"] if len(rows) == limit else None
        return jsonify(messages=messages, next_before_id=next_before_id), 200

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=False)
