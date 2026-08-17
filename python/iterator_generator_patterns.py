"""
Day 17 - Advanced Iterator and Generator Patterns

Covers:
- Iterator protocol
- Custom iterators
- Generator pipelines
- Lazy evaluation
- Generator composition
"""


class Countdown:
    """Simple custom iterator that counts down to zero."""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration

        value = self.current
        self.current -= 1
        return value


def numbers(limit: int):
    """Generate numbers lazily from 1 through limit."""
    for number in range(1, limit + 1):
        yield number


def squared(values):
    """Yield squares lazily."""
    for value in values:
        yield value * value


def even_only(values):
    """Yield only even values from an iterable."""
    for value in values:
        if value % 2 == 0:
            yield value


def generator_pipeline(limit: int):
    """Compose generators without materializing intermediate lists."""
    return squared(even_only(numbers(limit)))


if __name__ == "__main__":
    print("Custom iterator:")

    for value in Countdown(3):
        print(value)

    print("\nGenerator pipeline:")

    for value in generator_pipeline(10):
        print(value)