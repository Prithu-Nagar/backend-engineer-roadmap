-- ============================================
-- Database Normalization Practice
-- ============================================

-- Normalization Levels:
-- 1NF: Atomic values, no repeating groups
-- 2NF: 1NF + No partial dependencies
-- 3NF: 2NF + No transitive dependencies

-- ============================================
-- 1NF Violation Example - Repeating Groups
-- ============================================

-- BAD: Repeating columns (violates 1NF)
-- CREATE TABLE StudentCourses_Bad (
--     student_id INT,
--     student_name VARCHAR(50),
--     course1 VARCHAR(50),
--     course2 VARCHAR(50),
--     course3 VARCHAR(50)
-- );

-- GOOD: 1NF - Separate table for courses
CREATE TABLE Student_1NF (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE Course_1NF (
    course_id INT PRIMARY KEY,
    student_id INT,
    course_name VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Student_1NF(student_id)
);

-- ============================================
-- 2NF Violation Example - Partial Dependency
-- ============================================

-- BAD: Partial dependency (violates 2NF)
-- CREATE TABLE StudentCourses_Bad (
--     student_id INT,
--     course_id INT,
--     course_name VARCHAR(50),  -- Depends on course_id only, not on (student_id, course_id)
--     grade VARCHAR(2),
--     PRIMARY KEY (student_id, course_id)
-- );

-- GOOD: 2NF - Move dependent attributes to separate table
CREATE TABLE Course_2NF (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50)
);

CREATE TABLE Enrollment_2NF (
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (course_id) REFERENCES Course_2NF(course_id)
);

-- ============================================
-- 3NF Violation Example - Transitive Dependency
-- ============================================

-- BAD: Transitive dependency (violates 3NF)
-- CREATE TABLE Student_Bad (
--     student_id INT PRIMARY KEY,
--     student_name VARCHAR(50),
--     department_id INT,
--     department_name VARCHAR(50)  -- Depends on department_id, not directly on student_id
-- );

-- GOOD: 3NF - Remove transitive dependencies
CREATE TABLE Department_3NF (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

CREATE TABLE Student_3NF (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department_3NF(department_id)
);

-- ============================================
-- Example: Normalized E-Commerce Schema
-- ============================================

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10, 2),
    category_id INT
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- ============================================
-- Sample Queries on Normalized Schema
-- ============================================

-- Insert sample data
INSERT INTO Customers VALUES
(1, 'Alice Johnson', 'alice@example.com'),
(2, 'Bob Smith', 'bob@example.com');

INSERT INTO Categories VALUES
(1, 'Electronics'),
(2, 'Books');

INSERT INTO Products VALUES
(101, 'Laptop', 999.99, 1),
(102, 'Python Book', 49.99, 2);

INSERT INTO Orders VALUES
(1001, 1, '2024-01-15'),
(1002, 2, '2024-01-20');

INSERT INTO OrderItems VALUES
(1, 1001, 101, 1, 999.99),
(2, 1002, 102, 2, 49.99);

-- Query: Get customer orders with product details
SELECT
    c.customer_name,
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS total
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id;

-- Query: Get products by category
SELECT
    cat.category_name,
    p.product_name,
    p.price
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id;

-- ============================================
-- Denormalization Trade-offs
-- ============================================

/*
    Normalization reduces redundancy and improves
    data integrity.

    Denormalization intentionally introduces some
    redundancy to improve read performance or reduce
    expensive joins.

    Example:

    Normalized design:

    Customers
        |
        +---- Orders
                 |
                 +---- OrderItems
                           |
                           +---- Products

    A reporting query may require several joins.

    A denormalized reporting table can store commonly
    accessed information together.
*/

CREATE TABLE OrderSummary_Denormalized (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    order_date DATE,
    total_amount DECIMAL(12, 2)
);


-- Example denormalized data

INSERT INTO OrderSummary_Denormalized
(order_id, customer_id, customer_name, order_date, total_amount)
VALUES
(1001, 1, 'Alice Johnson', '2024-01-15', 999.99),
(1002, 2, 'Bob Smith', '2024-01-20', 99.98);


-- Query becomes simpler because frequently accessed
-- information is already stored together.

SELECT
    order_id,
    customer_name,
    order_date,
    total_amount
FROM OrderSummary_Denormalized
WHERE customer_id = 1;


-- ============================================
-- Normalization vs Denormalization
-- ============================================

/*
    Normalization advantages:
    - Less duplicated data
    - Better data integrity
    - Easier updates
    - Clear relationships

    Denormalization advantages:
    - Fewer joins
    - Faster read-heavy queries
    - Useful for reporting and analytics
    - Can simplify frequently executed queries

    Denormalization trade-offs:
    - More duplicated data
    - More storage
    - More complicated writes
    - Risk of inconsistent duplicated values

    General rule:

    Start with a normalized design.

    Introduce denormalization only when there is
    a measured performance or access-pattern reason.
*/