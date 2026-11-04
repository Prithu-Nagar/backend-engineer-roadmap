"""Password hashing and JWT authentication for the Task Manager API."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from functools import wraps
from typing import Any, TypeVar, cast

import jwt
from flask import current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

if __package__:
    from .extensions import db
    from .models import User
else:  # pragma: no cover - Docker runs modules as top-level imports
    from extensions import db
    from models import User

F = TypeVar("F", bound=Callable[..., Any])


def hash_password(password: str) -> str:
    """Hash a password with Werkzeug's PBKDF2-SHA256 password KDF."""
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)


def verify_password(password: str, password_hash: str) -> bool:
    """Compare a password with its stored password hash."""
    return check_password_hash(password_hash, password)


def create_access_token(user: User) -> str:
    """Create a signed, time-limited JWT for an existing user."""
    now = datetime.now(UTC)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(
            seconds=current_app.config["JWT_ACCESS_TOKEN_TTL_SECONDS"]
        ),
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256",
    )


def get_authenticated_user() -> User | None:
    """Validate the bearer token and load its current user from the database."""
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
            options={"require": ["sub", "iat", "exp"]},
        )
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        return None

    return db.session.get(User, user_id)


def login_required(function: F) -> F:
    """Reject requests without a valid bearer token."""
    @wraps(function)
    def wrapped(*args: Any, **kwargs: Any):
        user = get_authenticated_user()
        if user is None:
            return jsonify({
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "A valid bearer access token is required.",
                }
            }), 401
        g.current_user = user
        return function(*args, **kwargs)

    return cast(F, wrapped)
