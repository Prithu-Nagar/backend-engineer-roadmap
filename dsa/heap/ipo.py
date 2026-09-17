"""
LeetCode: IPO

Pattern:
Greedy selection with a max-heap after sorting projects by required capital.

Time Complexity:
O(n log n)

Space Complexity:
O(n)
"""

from __future__ import annotations

import heapq


class Solution:
    def findMaximizedCapital(
        self,
        k: int,
        w: int,
        profits: list[int],
        capital: list[int],
    ) -> int:
        projects = sorted(zip(capital, profits))
        max_heap: list[int] = []
        index = 0

        for _ in range(k):
            while index < len(projects) and projects[index][0] <= w:
                heapq.heappush(max_heap, -projects[index][1])
                index += 1

            if not max_heap:
                break

            w += -heapq.heappop(max_heap)

        return w


if __name__ == "__main__":
    solution = Solution()
    print(solution.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]))
