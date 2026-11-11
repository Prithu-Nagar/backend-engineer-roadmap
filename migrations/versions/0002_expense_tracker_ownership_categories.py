"""Create the Expense Tracker schema and enforce per-user ownership."""

import sqlalchemy as sa
from alembic import op

revision = "0002_expense_ownership_categories"
down_revision = "0001_create_users_tasks"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    op.create_table(
        "expense_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            ondelete="CASCADE",
            name="fk_expense_categories_owner_id_users",
        ),
        sa.UniqueConstraint(
            "owner_id", "name", name="uq_expense_category_owner_name"
        ),
        sa.CheckConstraint(
            "length(trim(name)) > 0", name="expense_category_name_check"
        ),
    )
    op.create_index(
        "idx_expense_categories_owner", "expense_categories", ["owner_id"]
    )

    if "expenses" not in existing_tables:
        op.create_table(
            "expenses",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("owner_id", sa.Integer(), nullable=False),
            sa.Column("amount", sa.Numeric(12, 2), nullable=False),
            sa.Column("category", sa.String(length=50), nullable=False),
            sa.Column("description", sa.String(length=255), nullable=True),
            sa.Column("expense_date", sa.Date(), nullable=False),
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
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["users.id"],
                ondelete="CASCADE",
                name="fk_expenses_owner_id_users",
            ),
            sa.CheckConstraint("amount > 0", name="expenses_amount_check"),
            sa.CheckConstraint(
                "length(trim(category)) > 0", name="expenses_category_check"
            ),
        )
    else:
        count = bind.execute(
            sa.text("SELECT COUNT(*) FROM expenses")
        ).scalar_one()
        if count:
            raise RuntimeError(
                "Existing expenses need an explicit owner_id backfill before "
                "this migration can enforce ownership. Backfill each row to "
                "its real user, then rerun the migration."
            )

        with op.batch_alter_table("expenses") as batch_op:
            batch_op.add_column(
                sa.Column("owner_id", sa.Integer(), nullable=True)
            )
            batch_op.create_foreign_key(
                "fk_expenses_owner_id_users",
                "users",
                ["owner_id"],
                ["id"],
                ondelete="CASCADE",
            )
            batch_op.alter_column(
                "owner_id", existing_type=sa.Integer(), nullable=False
            )

    existing_indexes = {
        index["name"] for index in sa.inspect(bind).get_indexes("expenses")
    }
    if "idx_expenses_category_date" not in existing_indexes:
        op.create_index(
            "idx_expenses_category_date",
            "expenses",
            ["category", "expense_date"],
        )
    if "idx_expenses_date" not in existing_indexes:
        op.create_index("idx_expenses_date", "expenses", ["expense_date"])
    op.create_index("idx_expenses_owner_id", "expenses", ["owner_id"])
    op.create_index(
        "idx_expenses_owner_category_date",
        "expenses",
        ["owner_id", "category", "expense_date"],
    )
    op.create_index(
        "idx_expenses_owner_date", "expenses", ["owner_id", "expense_date"]
    )


def downgrade():
    op.drop_index("idx_expenses_owner_date", table_name="expenses")
    op.drop_index(
        "idx_expenses_owner_category_date", table_name="expenses"
    )
    op.drop_index("idx_expenses_owner_id", table_name="expenses")
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.drop_constraint("fk_expenses_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")
    op.drop_index(
        "idx_expense_categories_owner", table_name="expense_categories"
    )
    op.drop_table("expense_categories")
