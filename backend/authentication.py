"""
Authentication utilities for the Task Manager backend.

Day 11:
- Authentication fundamentals
- JWT authentication
- Access tokens
- Token validation

Day 12:
- Authorization is handled separately from authentication.
"""

import hashlib
import hmac
import os
import time
from typing import Optional

import jwt


JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_SECONDS = 3600

JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "development-secret-change-in-production",
)


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    Production applications should use a password-specific
    hashing algorithm such as bcrypt or Argon2.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its stored hash.
    """
    calculated_hash = hash_password(password)

    return hmac.compare_digest(
        calculated_hash,
        password_hash,
    )


def create_access_token(
    user_id: int,
    username: str,
    role: str = "user",
) -> str:
    """
    Create a JWT access token containing the user's identity and role.
    """
    now = int(time.time())

    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + JWT_EXPIRATION_SECONDS,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[dict]:
    """
    Validate and decode a JWT access token.

    Returns the decoded payload when the token is valid.
    Returns None when the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


def authenticate_user(
    username: str,
    password: str,
    users: dict,
) -> Optional[dict]:
    """
    Authenticate a user against a simple in-memory user store.

    Returns the user data when authentication succeeds.
    """
    user = users.get(username)

    if not user:
        return None

    if not verify_password(
        password,
        user["password_hash"],
    ):
        return None

    return user


if __name__ == "__main__":
    users = {
        "alice": {
            "user_id": 1,
            "username": "alice",
            "role": "user",
            "password_hash": hash_password("password123"),
        }
    }

    user = authenticate_user(
        "alice",
        "password123",
        users,
    )

    if user:
        token = create_access_token(
            user["user_id"],
            user["username"],
            user["role"],
        )

        print("Access token created.")
        print("Decoded token:", decode_access_token(token))
    else:
        print("Authentication failed.")
