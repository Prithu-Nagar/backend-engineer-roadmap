"""
Lambda Function Examples
"""

nums = [1, 2, 3, 4, 5]

print([x * x for x in nums])

print(list(filter(lambda x: x % 2 == 0, nums)))

students = [
    ("Alice", 90),
    ("Bob", 70),
    ("Charlie", 85)
]

students.sort(key=lambda student: student[1])

print(students)