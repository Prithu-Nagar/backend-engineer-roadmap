"""SQLAlchemy models for the Task Manager MVP."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, Index, UniqueConstraint, func
from sqlalchemy.orm import validates

if __package__:
    from .extensions import db
else:  # pragma: no cover - Docker runs app.py as a top-level module
    from extensions import db


class User(db.Model):
    """An account that owns tasks and authenticates with a password hash."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="users_role_check"),
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(20), nullable=False, default="user", server_default="user"
    )
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    tasks = db.relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @validates("username", "email")
    def normalize_identity(self, key: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        return value.strip().lower() if key == "email" else value.strip()

    @validates("role")
    def validate_role(self, _key: str, value: str) -> str:
        if value not in {"user", "admin"}:
            raise ValueError("role must be 'user' or 'admin'")
        return value


class Task(db.Model):
    """A task belonging to exactly one user."""

    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("length(trim(title)) > 0", name="tasks_title_check"),
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed')",
            name="tasks_status_check",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="tasks_priority_check",
        ),
        Index("idx_tasks_user_status", "user_id", "status"),
        Index("idx_tasks_user_priority", "user_id", "priority"),
        Index("idx_tasks_created_at", "created_at"),
        Index("idx_tasks_user_id", "user_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE", name="tasks_user_fk"),
        nullable=False,
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), nullable=False, default="pending", server_default="pending"
    )
    priority = db.Column(
        db.String(20), nullable=False, default="medium", server_default="medium"
    )
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=lambda: datetime.now(UTC),
    )
    owner = db.relationship("User", back_populates="tasks")

    @validates("title")
    def validate_title(self, _key: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string")
        value = value.strip()
        if len(value) > 200:
            raise ValueError("title must be at most 200 characters")
        return value

    @validates("status")
    def validate_status(self, _key: str, value: str) -> str:
        if value not in {"pending", "in_progress", "completed"}:
            raise ValueError("status is not supported")
        return value

    @validates("priority")
    def validate_priority(self, _key: str, value: str) -> str:
        if value not in {"low", "medium", "high"}:
            raise ValueError("priority is not supported")
        return value
