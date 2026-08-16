"""
Day 16 - Hashing: Sets and Collision Intuition

Topics:
- Set membership
- Hash-based lookup
- Duplicate detection
- Hash collision intuition
"""


def contains_duplicate(values):
    """Return True if the input contains duplicates."""
    seen = set()

    for value in values:
        if value in seen:
            return True

        seen.add(value)

    return False


def unique_values(values):
    """Return unique values while preserving first-seen order."""
    seen = set()
    result = []

    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)

    return result


def has_pair_with_sum(values, target):
    """Return True if two different values sum to target."""
    seen = set()

    for value in values:
        complement = target - value

        if complement in seen:
            return True

        seen.add(value)

    return False


if __name__ == "__main__":
    values = [1, 2, 3, 2, 5]

    print("Contains duplicate:", contains_duplicate(values))
    print("Unique values:", unique_values(values))
    print("Pair with sum 7:", has_pair_with_sum(values, 7))