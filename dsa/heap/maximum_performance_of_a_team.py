"""
LeetCode: Maximum Performance of a Team

Pattern:
Sort engineers by efficiency and maintain the best k speeds in a min-heap.
The current efficiency acts as the limiting factor for the team.

Time Complexity:
O(n log k)

Space Complexity:
O(k)
"""

from __future__ import annotations

import heapq


class Solution:
    def maxPerformance(
        self,
        n: int,
        speed: list[int],
        efficiency: list[int],
        k: int,
    ) -> int:
        engineers = sorted(
            zip(efficiency, speed),
            reverse=True,
        )

        speed_heap: list[int] = []
        speed_sum = 0
        best = 0
        modulo = 10**9 + 7

        for current_efficiency, current_speed in engineers:
            heapq.heappush(speed_heap, current_speed)
            speed_sum += current_speed

            if len(speed_heap) > k:
                speed_sum -= heapq.heappop(speed_heap)

            best = max(best, speed_sum * current_efficiency)

        return best % modulo


if __name__ == "__main__":
    solution = Solution()
    print(solution.maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2))
