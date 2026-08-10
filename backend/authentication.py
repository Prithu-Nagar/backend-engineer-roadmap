"""
Flask Authentication Basics

Demonstrates:
- Password hashing
- Password verification
- Basic authentication flow
- Protecting an endpoint with a decorator

This is a learning example and is not intended to be
used as a production authentication system.
"""

from functools import wraps

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)


users = {
    "admin": generate_password_hash("demo-password"),
}


def authenticate(username: str, password: str) -> bool:
    """Validate a username and password."""
    password_hash = users.get(username)

    if password_hash is None:
        return False

    return check_password_hash(password_hash, password)


def require_authentication(view):
    """Protect an endpoint using HTTP Basic Authentication."""

    @wraps(view)
    def decorated_view(*args, **kwargs):
        auth = request.authorization

        if auth is None or not authenticate(auth.username, auth.password):
            return (
                jsonify({"error": "Authentication required"}),
                401,
                {
                    "WWW-Authenticate": 'Basic realm="Login Required"'
                },
            )

        return view(*args, **kwargs)

    return decorated_view


@app.route("/public", methods=["GET"])
def public_endpoint():
    """Endpoint that does not require authentication."""
    return jsonify({"message": "Public endpoint"}), 200


@app.route("/protected", methods=["GET"])
@require_authentication
def protected_endpoint():
    """Endpoint protected by authentication."""
    return jsonify({"message": "Authenticated request"}), 200


if __name__ == "__main__":
    app.run(debug=True)
