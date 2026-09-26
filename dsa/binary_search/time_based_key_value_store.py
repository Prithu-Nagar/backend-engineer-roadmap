"""
LeetCode: Time Based Key-Value Store

Day 57 — Binary Search / Intervals

Store values by timestamp and retrieve the value whose timestamp is the
largest timestamp less than or equal to the requested timestamp.
"""

from __future__ import annotations

from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self._store: dict[str, list[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self._store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        entries = self._store.get(key, [])
        left, right = 0, len(entries) - 1
        answer = ""

        while left <= right:
            mid = left + (right - left) // 2
            mid_timestamp, mid_value = entries[mid]

            if mid_timestamp <= timestamp:
                answer = mid_value
                left = mid + 1
            else:
                right = mid - 1

        return answer


if __name__ == "__main__":
    time_map = TimeMap()
    time_map.set("foo", "bar", 1)
    time_map.set("foo", "bar2", 4)

    print(time_map.get("foo", 1))
    print(time_map.get("foo", 3))
    print(time_map.get("foo", 4))
