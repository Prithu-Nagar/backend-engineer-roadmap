"""
Higher-Order Functions in Python

A Higher-Order Function is a function that:
1. Accepts another function as an argument
OR
2. Returns another function
"""

from functools import reduce


def square(x):
    return x * x


def cube(x):
    return x ** 3


def apply_operation(func, value):
    return func(value)


print("Square of 5:", apply_operation(square, 5))
print("Cube of 5:", apply_operation(cube, 5))


numbers = [1, 2, 3, 4, 5]

# map()
squares = list(map(square, numbers))
print("\nSquares:", squares)

# filter()
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even Numbers:", even_numbers)

# reduce()
total = reduce(lambda x, y: x + y, numbers)
print("Sum:", total)

# sorted()
students = [
    ("Alice", 92),
    ("Bob", 81),
    ("Charlie", 95),
    ("David", 88)
]

sorted_students = sorted(students, key=lambda student: student[1])

print("\nStudents Sorted by Marks:")
for name, marks in sorted_students:
    print(f"{name}: {marks}")