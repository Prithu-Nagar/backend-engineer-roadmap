"""
Exception Handling Examples
"""


def basic_try_except():
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero.")


def multiple_exceptions(value):
    try:
        number = int(value)
        result = 100 / number
        print(result)

    except ValueError:
        print("Please enter a valid integer.")

    except ZeroDivisionError:
        print("Division by zero is not allowed.")


def generic_exception():
    try:
        value = int("Python")
    except Exception as e:
        print("Error:", e)


def try_except_else(value):
    try:
        age = int(value)

    except ValueError:
        print("Invalid input.")

    else:
        print(f"Age entered: {age}")


def finally_example():
    try:
        file = open("sample.txt", "r")

    except FileNotFoundError:
        print("File not found.")

    finally:
        print("Execution completed.")


def raise_exception(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")

    return age


class InvalidAgeError(Exception):
    """Raised when age is invalid."""


def custom_exception(age):
    if age < 0:
        raise InvalidAgeError("Invalid age entered.")

    return age


def index_error_example():
    numbers = [1, 2, 3]

    try:
        print(numbers[5])

    except IndexError:
        print("Index out of range.")


def key_error_example():
    student = {
        "name": "Alice"
    }

    try:
        print(student["age"])

    except KeyError:
        print("Key does not exist.")


def type_error_example():
    try:
        print("10" + 5)

    except TypeError:
        print("Cannot concatenate string and integer.")


def divide(a, b):
    """
    Returns division result.

    Raises:
        ZeroDivisionError: If denominator is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Denominator cannot be zero.")

    return a / b


if __name__ == "__main__":
    basic_try_except()

    multiple_exceptions("25")
    multiple_exceptions("0")
    multiple_exceptions("abc")

    generic_exception()

    try_except_else("22")
    try_except_else("abc")

    finally_example()

    try:
        raise_exception(-5)
    except ValueError as e:
        print(e)

    try:
        custom_exception(-10)
    except InvalidAgeError as e:
        print(e)

    index_error_example()

    key_error_example()

    type_error_example()

    try:
        print(divide(20, 4))
        print(divide(20, 0))
    except ZeroDivisionError as e:
        print(e)