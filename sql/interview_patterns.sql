-- ============================================
-- DAY 18 SQL
-- Top-N, Latest Row, Duplicate Detection
-- ============================================


-- ============================================
-- 1. TOP-N
-- ============================================

-- Top 5 highest-paid employees

SELECT
    employee_id,
    name,
    salary
FROM employees
ORDER BY salary DESC
LIMIT 5;


-- ============================================
-- 2. TOP-N PER GROUP
-- ============================================

-- Highest-paid employee in each department

SELECT
    employee_id,
    name,
    department_id,
    salary
FROM (
    SELECT
        employee_id,
        name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rn
    FROM employees
) ranked
WHERE rn = 1;


-- ============================================
-- 3. LATEST ROW
-- ============================================

-- Latest employee record

SELECT
    employee_id,
    name,
    updated_at
FROM employees
ORDER BY updated_at DESC
LIMIT 1;


-- ============================================
-- 4. LATEST ROW PER GROUP
-- ============================================

SELECT
    employee_id,
    name,
    department_id,
    updated_at
FROM (
    SELECT
        employee_id,
        name,
        department_id,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM employees
) ranked
WHERE rn = 1;


-- ============================================
-- 5. DUPLICATE DETECTION
-- ============================================

-- Find duplicate email addresses

SELECT
    email,
    COUNT(*) AS occurrence_count
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;


-- ============================================
-- 6. DUPLICATE ROWS
-- ============================================

SELECT
    name,
    department_id,
    COUNT(*) AS occurrence_count
FROM employees
GROUP BY
    name,
    department_id
HAVING COUNT(*) > 1;