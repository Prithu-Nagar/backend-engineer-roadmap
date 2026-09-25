"""
LeetCode: Minimum Number of Refueling Stops

Pattern:
Greedy selection with a max-heap of fuel available from stations already
reachable.

Time Complexity:
O(n log n)

Space Complexity:
O(n)
"""

from __future__ import annotations

import heapq


class Solution:
    def minRefuelStops(
        self,
        target: int,
        startFuel: int,
        stations: list[list[int]],
    ) -> int:
        max_heap: list[int] = []
        fuel = startFuel
        previous = 0
        stops = 0

        for position, station_fuel in stations + [[target, 0]]:
            fuel -= position - previous

            while fuel < 0 and max_heap:
                fuel += -heapq.heappop(max_heap)
                stops += 1

            if fuel < 0:
                return -1

            heapq.heappush(max_heap, -station_fuel)
            previous = position

        return stops


if __name__ == "__main__":
    solution = Solution()
    print(solution.minRefuelStops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]))
