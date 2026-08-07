/*
    SQL Indexes

    Topics:
    - Creating indexes
    - Unique indexes
    - Composite indexes
    - Index usage
    - Removing indexes
    - Query execution plans
*/


-- ---------------------------------------
-- Sample Table
-- ---------------------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    age INT
);


-- ---------------------------------------
-- Basic Index
-- ---------------------------------------

CREATE INDEX idx_users_email
ON users(email);


-- ---------------------------------------
-- Query Using an Indexed Column
-- ---------------------------------------

SELECT *
FROM users
WHERE email = 'user@example.com';


-- ---------------------------------------
-- Unique Index
-- ---------------------------------------

CREATE UNIQUE INDEX idx_users_unique_email
ON users(email);


-- ---------------------------------------
-- Composite Index
-- ---------------------------------------

CREATE INDEX idx_users_city_age
ON users(city, age);


-- ---------------------------------------
-- Query Using Composite Index
-- ---------------------------------------

SELECT *
FROM users
WHERE city = 'Lucknow'
  AND age = 25;


-- ---------------------------------------
-- Index Column Order
-- ---------------------------------------

/*
    For an index on:

        (city, age)

    queries filtering by city can benefit from
    the index.

    Queries filtering only by age may not benefit
    from this composite index in the same way.
*/

SELECT *
FROM users
WHERE city = 'Lucknow';


-- ---------------------------------------
-- EXPLAIN
-- ---------------------------------------

EXPLAIN
SELECT *
FROM users
WHERE email = 'user@example.com';


-- ---------------------------------------
-- EXPLAIN ANALYZE
-- ---------------------------------------

EXPLAIN ANALYZE
SELECT *
FROM users
WHERE city = 'Lucknow';


-- ---------------------------------------
-- Dropping an Index
-- ---------------------------------------

DROP INDEX idx_users_city_age;