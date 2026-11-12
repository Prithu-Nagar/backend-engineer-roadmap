"""Add owner-scoped monthly category budgets."""

import sqlalchemy as sa
from alembic import op

revision = "0003_expense_budgets"
down_revision = "0002_expense_ownership_categories"
branch_labels = None
depends_on = None


def upgrade():
    month_start_check = (
        "CAST(strftime('%d', month_start) AS INTEGER) = 1"
        if op.get_bind().dialect.name == "sqlite"
        else "EXTRACT(DAY FROM month_start) = 1"
    )
    op.create_table(
        "expense_budgets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("month_start", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
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
            name="fk_expense_budgets_owner_id_users",
        ),
        sa.UniqueConstraint(
            "owner_id",
            "category",
            "month_start",
            name="uq_expense_budget_owner_category_month",
        ),
        sa.CheckConstraint("amount > 0", name="expense_budget_amount_check"),
        sa.CheckConstraint(
            "length(trim(category)) > 0", name="expense_budget_category_check"
        ),
        sa.CheckConstraint(
            month_start_check, name="expense_budget_month_start_check"
        ),
    )
    op.create_index(
        "idx_expense_budgets_owner_month",
        "expense_budgets",
        ["owner_id", "month_start"],
    )


def downgrade():
    op.drop_index(
        "idx_expense_budgets_owner_month", table_name="expense_budgets"
    )
    op.drop_table("expense_budgets")
