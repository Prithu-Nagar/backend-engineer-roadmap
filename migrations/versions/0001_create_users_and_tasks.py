"""Create the Task Manager users and tasks tables."""

import sqlalchemy as sa
from alembic import op

revision = "0001_create_users_tasks"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), server_default="user", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("role IN ('user', 'admin')", name="users_role_check"),
        sa.UniqueConstraint("username", name="uq_users_username"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status", sa.String(length=20), server_default="pending", nullable=False
        ),
        sa.Column(
            "priority", sa.String(length=20), server_default="medium", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("length(trim(title)) > 0", name="tasks_title_check"),
        sa.CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed')",
            name="tasks_status_check",
        ),
        sa.CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="tasks_priority_check",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE", name="tasks_user_fk"
        ),
    )
    op.create_index("idx_tasks_user_id", "tasks", ["user_id"], unique=False)
    op.create_index(
        "idx_tasks_user_status", "tasks", ["user_id", "status"], unique=False
    )
    op.create_index(
        "idx_tasks_user_priority", "tasks", ["user_id", "priority"], unique=False
    )
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"], unique=False)


def downgrade():
    op.drop_index("idx_tasks_created_at", table_name="tasks")
    op.drop_index("idx_tasks_user_priority", table_name="tasks")
    op.drop_index("idx_tasks_user_status", table_name="tasks")
    op.drop_index("idx_tasks_user_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("users")
