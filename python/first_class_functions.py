"""
First-Class Functions in Python

Functions can:
1. Be assigned to variables
2. Be passed as arguments
3. Be returned from other functions
"""


def greet():
    return "Hello, World!"


# Assign to variable
say_hello = greet

print(say_hello())


# Pass function as argument
def execute(func):
    print(func())


execute(greet)


# Return function
def choose_operation(operation):
    if operation == "square":
        return lambda x: x * x
    elif operation == "cube":
        return lambda x: x ** 3
    else:
        return lambda x: x


square = choose_operation("square")
cube = choose_operation("cube")

print(square(5))
print(cube(3))