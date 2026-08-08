"""
Python Closures

Demonstrates how an inner function can retain access
to variables from its enclosing function.
"""


def multiplier(factor):
    def multiply(number):
        return number * factor

    return multiply


if __name__ == "__main__":
    double = multiplier(2)
    triple = multiplier(3)

    print("Double:", double(5))
    print("Triple:", triple(5))
