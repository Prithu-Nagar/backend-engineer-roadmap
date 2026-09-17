"""
LeetCode: Furthest Building You Can Reach

Pattern:
Use ladders for the largest climbs and a min-heap to keep the smaller climbs
paid for with bricks.

Time Complexity:
O(n log n)

Space Complexity:
O(n)
"""

from __future__ import annotations

import heapq


class Solution:
    def furthestBuilding(
        self,
        heights: list[int],
        bricks: int,
        ladders: int,
    ) -> int:
        climbs: list[int] = []

        for index in range(len(heights) - 1):
            climb = heights[index + 1] - heights[index]
            if climb <= 0:
                continue

            heapq.heappush(climbs, climb)

            if len(climbs) > ladders:
                bricks -= heapq.heappop(climbs)

            if bricks < 0:
                return index

        return len(heights) - 1


if __name__ == "__main__":
    solution = Solution()
    print(solution.furthestBuilding([4, 2, 7, 6, 9, 14, 12], 5, 1))
