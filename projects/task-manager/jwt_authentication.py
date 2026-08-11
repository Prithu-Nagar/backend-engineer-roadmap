"""
JWT authentication helpers for the Task Manager API.
"""

from datetime import datetime, timedelta, timezone
import os

import jwt


JWT_SECRET = os.getenv("JWT_SECRET", "development-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30


def create_access_token(user_id):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )