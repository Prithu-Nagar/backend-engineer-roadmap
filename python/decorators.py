"""
Python Decorators
"""

from functools import wraps
import time


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} completed")
        return result

    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(f"Execution Time: {end - start:.6f} seconds")

        return result

    return wrapper


@logger
@timer
def greet(name):
    print(f"Hello, {name}!")


@timer
def calculate_square(n):
    return n * n


if __name__ == "__main__":

    greet("Prithu")

    print()

    result = calculate_square(25)

    print("Square:", result)