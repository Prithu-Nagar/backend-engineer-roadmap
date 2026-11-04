"""Registration, login, and identity endpoints for the Task Manager."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

if __package__:
    from .auth import (
        create_access_token,
        hash_password,
        login_required,
        verify_password,
    )
    from .extensions import db
    from .models import User
else:  # pragma: no cover - Docker runs modules as top-level imports
    from auth import create_access_token, hash_password, login_required, verify_password
    from extensions import db
    from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    """Create a regular user account; public registration cannot grant admin."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "A JSON object is required."}}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all(isinstance(value, str) and value.strip() for value in (username, email, password)):
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Username, email, and password are required."}}), 400
    if len(username.strip()) > 100 or len(email.strip()) > 255:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Username or email is too long."}}), 400
    if len(password) < current_app.config["PASSWORD_MIN_LENGTH"]:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": f"Password must contain at least {current_app.config['PASSWORD_MIN_LENGTH']} characters."}}), 400

    normalized_email = email.strip().lower()
    normalized_username = username.strip()
    existing = User.query.filter(
        or_(User.username == normalized_username, User.email == normalized_email)
    ).first()
    if existing:
        return jsonify({"error": {"code": "ACCOUNT_EXISTS", "message": "Username or email is already registered."}}), 409

    user = User(
        username=normalized_username,
        email=normalized_email,
        password_hash=hash_password(password),
        role="user",
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": {"code": "ACCOUNT_EXISTS", "message": "Username or email is already registered."}}), 409

    return jsonify({
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 201


@auth_bp.post("/login")
def login():
    """Verify credentials and return a short-lived JWT access token."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid username/email or password."}}), 401

    identity = data.get("username") or data.get("email")
    password = data.get("password")
    if not isinstance(identity, str) or not isinstance(password, str):
        return jsonify({"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid username/email or password."}}), 401

    user = User.query.filter(
        or_(User.username == identity.strip(), User.email == identity.strip().lower())
    ).first()
    if user is None or not verify_password(password, user.password_hash):
        return jsonify({"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid username/email or password."}}), 401

    return jsonify({
        "access_token": create_access_token(user),
        "token_type": "Bearer",
        "expires_in": current_app.config["JWT_ACCESS_TOKEN_TTL_SECONDS"],
    }), 200


@auth_bp.get("/me")
@login_required
def me():
    """Return the identity associated with the validated token."""
    user = g.current_user
    return jsonify({
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 200
