"""
Topic: Generators

Description:
Demonstrates Python generators, the yield keyword, and lazy evaluation.

Run:
python generators.py
"""


def count_up_to(n):
    """
    Generates numbers from 1 to n.
    """

    count = 1

    while count <= n:
        yield count
        count += 1


def fibonacci(limit):
    """
    Generates Fibonacci numbers.
    """

    first, second = 0, 1

    for _ in range(limit):
        yield first
        first, second = second, first + second


def even_numbers(limit):
    """
    Generates even numbers up to the given limit.
    """

    for number in range(limit + 1):
        if number % 2 == 0:
            yield number


if __name__ == "__main__":

    print("Count Generator")
    for number in count_up_to(5):
        print(number)

    print("\nFibonacci Generator")
    for number in fibonacci(10):
        print(number)

    print("\nEven Number Generator")
    for number in even_numbers(10):
        print(number)