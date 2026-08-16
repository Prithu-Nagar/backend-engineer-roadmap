"""
Day 16 - Hashing: Frequency Maps

Topics:
- Frequency counting
- Dictionary-based hashing
- O(1) average lookup
- Counting occurrences
"""


def build_frequency_map(values):
    """Return a frequency map for the given values."""
    frequency = {}

    for value in values:
        frequency[value] = frequency.get(value, 0) + 1

    return frequency


def most_frequent(values):
    """Return the most frequent value.

    If multiple values have the same frequency, the first one
    encountered is returned.
    """
    if not values:
        return None

    frequency = build_frequency_map(values)

    best_value = values[0]
    best_count = frequency[best_value]

    for value in values:
        if frequency[value] > best_count:
            best_value = value
            best_count = frequency[value]

    return best_value


def first_unique(values):
    """Return the first value that occurs exactly once."""
    frequency = build_frequency_map(values)

    for value in values:
        if frequency[value] == 1:
            return value

    return None


if __name__ == "__main__":
    numbers = [1, 2, 2, 3, 3, 3, 4]

    print("Frequency:", build_frequency_map(numbers))
    print("Most frequent:", most_frequent(numbers))
    print("First unique:", first_unique(numbers))