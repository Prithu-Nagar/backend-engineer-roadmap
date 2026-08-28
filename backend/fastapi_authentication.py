"""
Day 28 — FastAPI Authentication with OAuth2 and JWT Concepts

Demonstrates:
- OAuth2 bearer-token dependency
- JWT access-token creation and validation
- authentication vs authorization boundaries
- protecting a FastAPI endpoint

This is a learning example. Production services should use a strong secret
from a secure secret manager and a real identity store/provider.
"""

from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


app = FastAPI(title="FastAPI Authentication Example")

JWT_ALGORITHM = "HS256"
JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "development-only-secret-change-me",
)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user_id: int) -> str:
    """Create a short-lived JWT access token."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT, raising 401 for invalid tokens."""
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    """Authenticate the request and return the token subject."""
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject is missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id}


@app.get("/api/me")
def read_current_user(
    current_user: dict[str, str] = Depends(get_current_user),
) -> dict[str, dict[str, str]]:
    """Return the authenticated user's identity."""
    return {"user": current_user}


if __name__ == "__main__":
    demo_token = create_access_token(101)
    print("Demo access token created.")
    print("Decoded payload:", decode_access_token(demo_token))
