"""
Python Dataclasses

Day 15 focus:
- Dataclass decorator
- Automatic __init__, __repr__, __eq__
- Field defaults
- Immutability with frozen
- Post-init processing
- Comparison methods
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    """Simple dataclass with basic fields."""

    x: float
    y: float


@dataclass
class Person:
    """Dataclass with defaults and post-init processing."""

    name: str
    age: int
    email: str = ""
    hobbies: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate and process data after initialization."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if not self.email:
            self.email = f"{self.name.lower()}@example.com"


@dataclass(frozen=True)
class ImmutableConfig:
    """Immutable dataclass (frozen)."""

    host: str
    port: int
    debug: bool = False


@dataclass(order=True)
class Student:
    """Dataclass with ordering enabled."""

    name: str
    gpa: float = field(compare=True)
    student_id: int = field(compare=False)


if __name__ == "__main__":
    # Basic usage
    p = Point(3.0, 4.0)
    print(f"Point: {p}")

    # With defaults and post-init
    person = Person("Alice", 30)
    print(f"Person: {person}")

    # Immutable
    config = ImmutableConfig("localhost", 8000)
    print(f"Config: {config}")

    # Ordering
    student1 = Student("Alice", 3.8, 1)
    student2 = Student("Bob", 3.5, 2)
    print(f"student1 > student2: {student1 > student2}")
