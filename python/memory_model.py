"""
Day 16 - Python Memory Model

Topics:
- Object references
- Identity vs equality
- Mutability
- Assignment
- Shallow copy
- Deep copy
"""

from copy import copy, deepcopy


def demonstrate_references():
    """Demonstrate that assignment creates another reference."""
    original = [1, 2, 3]
    alias = original

    alias.append(4)

    return original, alias


def demonstrate_mutability():
    """Demonstrate mutation of a mutable object."""
    values = [1, 2, 3]

    def add_value(items):
        items.append(4)

    add_value(values)

    return values


def demonstrate_shallow_copy():
    """Demonstrate shallow copying of nested structures."""
    original = [[1, 2], [3, 4]]
    copied = copy(original)

    copied[0].append(99)

    return original, copied


def demonstrate_deep_copy():
    """Demonstrate independent nested objects."""
    original = [[1, 2], [3, 4]]
    copied = deepcopy(original)

    copied[0].append(99)

    return original, copied


def demonstrate_identity_vs_equality():
    """Show the difference between == and is."""
    first = [1, 2, 3]
    second = [1, 2, 3]
    third = first

    return {
        "first == second": first == second,
        "first is second": first is second,
        "first is third": first is third,
    }


if __name__ == "__main__":
    print("References:", demonstrate_references())
    print("Mutability:", demonstrate_mutability())
    print("Shallow copy:", demonstrate_shallow_copy())
    print("Deep copy:", demonstrate_deep_copy())
    print("Identity vs equality:", demonstrate_identity_vs_equality())