-- Day 36 — PostgreSQL Full-Text Search
--
-- PostgreSQL full-text search converts text into searchable lexemes and can
-- use a GIN index for efficient matching. This is useful for searching
-- free-form fields such as expense descriptions.

-- Search directly with to_tsvector() and plainto_tsquery().
SELECT id, category, description, expense_date
FROM expenses
WHERE to_tsvector(
          'english',
          coalesce(category, '') || ' ' || coalesce(description, '')
      ) @@ plainto_tsquery('english', 'flight hotel');

-- A GIN expression index avoids building the search vector for every row
-- during a typical indexed search.
CREATE INDEX IF NOT EXISTS idx_expenses_full_text
    ON expenses
    USING GIN (
        to_tsvector(
            'english',
            coalesce(category, '') || ' ' || coalesce(description, '')
        )
    );

-- With the index in place, the same search can use the indexed expression.
EXPLAIN
SELECT id, category, description
FROM expenses
WHERE to_tsvector(
          'english',
          coalesce(category, '') || ' ' || coalesce(description, '')
      ) @@ plainto_tsquery('english', 'flight hotel');

-- tsquery operators can express more precise searches.
SELECT id, category, description
FROM expenses
WHERE to_tsvector(
          'english',
          coalesce(category, '') || ' ' || coalesce(description, '')
      ) @@ to_tsquery('english', 'flight & hotel');

-- ts_rank() can rank matching rows by relevance.
SELECT id,
       category,
       description,
       ts_rank(
           to_tsvector(
               'english',
               coalesce(category, '') || ' ' || coalesce(description, '')
           ),
           plainto_tsquery('english', 'flight hotel')
       ) AS rank
FROM expenses
WHERE to_tsvector(
          'english',
          coalesce(category, '') || ' ' || coalesce(description, '')
      ) @@ plainto_tsquery('english', 'flight hotel')
ORDER BY rank DESC;

-- Operational notes:
-- 1. GIN indexes can improve search performance but increase write/storage cost.
-- 2. Choose the text-search configuration according to the application's language.
-- 3. Use full-text search for linguistic matching, not arbitrary substring search.
-- 4. Measure query plans with representative data before adding an index.
