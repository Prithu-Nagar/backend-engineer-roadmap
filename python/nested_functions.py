"""
Nested Functions in Python

A nested function is a function defined inside another function.
Nested functions help organize code and are the foundation for closures.
"""


def outer():
    print("Inside outer function")

    def inner():
        print("Inside inner function")

    inner()


outer()

print("-" * 40)


def calculator(a, b):
    def add():
        return a + b

    def subtract():
        return a - b

    def multiply():
        return a * b

    def divide():
        if b == 0:
            return "Cannot divide by zero"
        return a / b

    print(f"{a} + {b} = {add()}")
    print(f"{a} - {b} = {subtract()}")
    print(f"{a} * {b} = {multiply()}")
    print(f"{a} / {b} = {divide()}")


calculator(20, 5)

print("-" * 40)


def greet(name):
    def message():
        return f"Hello, {name}!"

    return message()


print(greet("Prithu"))