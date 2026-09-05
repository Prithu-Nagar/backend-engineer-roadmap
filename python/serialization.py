"""
Day 36 — Python Serialization

Demonstrates JSON serialization for interoperable data and pickle concepts
for Python-specific object persistence. Pickle should not be used with
untrusted input because unpickling can execute arbitrary code.
"""

from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass


@dataclass
class Expense:
    """Simple serializable domain object."""

    expense_id: int
    category: str
    amount: float


def to_json(expense: Expense) -> str:
    """Serialize an Expense into a JSON string."""
    return json.dumps(asdict(expense), sort_keys=True)


def from_json(payload: str) -> Expense:
    """Deserialize an Expense from JSON with explicit field mapping."""
    data = json.loads(payload)
    return Expense(
        expense_id=int(data["expense_id"]),
        category=str(data["category"]),
        amount=float(data["amount"]),
    )


def to_pickle(expense: Expense) -> bytes:
    """Serialize an object with pickle for trusted Python-only use."""
    return pickle.dumps(expense)


def from_pickle(payload: bytes) -> Expense:
    """Deserialize trusted pickle data.

    Never unpickle data received from an untrusted source.
    """
    value = pickle.loads(payload)
    if not isinstance(value, Expense):
        raise TypeError("unexpected object type in pickle payload")
    return value


if __name__ == "__main__":
    expense = Expense(expense_id=1001, category="travel", amount=2500.0)

    json_payload = to_json(expense)
    print(json_payload)
    print(from_json(json_payload))

    pickle_payload = to_pickle(expense)
    print(from_pickle(pickle_payload))
