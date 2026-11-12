-- Expense Tracker relational schema (PostgreSQL)

CREATE TABLE expense_categories (
    id BIGSERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_expense_category_owner_name UNIQUE (owner_id, name),
    CONSTRAINT expense_category_name_check CHECK (length(trim(name)) > 0)
);

CREATE INDEX idx_expense_categories_owner
    ON expense_categories (owner_id);

CREATE TABLE expenses (
    id BIGSERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    expense_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT expense_category_check CHECK (length(trim(category)) > 0)
);

CREATE INDEX idx_expenses_category_date
    ON expenses (category, expense_date DESC);

CREATE INDEX idx_expenses_date
    ON expenses (expense_date DESC);

CREATE INDEX idx_expenses_owner_id
    ON expenses (owner_id);

CREATE INDEX idx_expenses_owner_category_date
    ON expenses (owner_id, category, expense_date DESC);

CREATE INDEX idx_expenses_owner_date
    ON expenses (owner_id, expense_date DESC);


CREATE TABLE expense_budgets (
    id BIGSERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    month_start DATE NOT NULL CHECK (EXTRACT(DAY FROM month_start) = 1),
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_expense_budget_owner_category_month
        UNIQUE (owner_id, category, month_start),
    CONSTRAINT expense_budget_category_check
        CHECK (length(trim(category)) > 0)
);

CREATE INDEX idx_expense_budgets_owner_month
    ON expense_budgets (owner_id, month_start);
