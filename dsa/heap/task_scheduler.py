"""
LeetCode: Task Scheduler

Pattern:
Max-heap + greedy scheduling in cycles of n + 1 slots.

Time Complexity:
O(T log K), where T is the number of tasks and K is the number of distinct
task types.

Space Complexity:
O(K)
"""

from __future__ import annotations

from collections import Counter
import heapq


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        if not tasks:
            return 0

        frequencies = Counter(tasks)
        max_heap = [-count for count in frequencies.values()]
        heapq.heapify(max_heap)

        elapsed = 0

        while max_heap:
            cycle: list[int] = []
            slots_used = 0

            for _ in range(n + 1):
                if not max_heap:
                    break

                remaining = -heapq.heappop(max_heap) - 1
                if remaining > 0:
                    cycle.append(remaining)
                slots_used += 1

            for remaining in cycle:
                heapq.heappush(max_heap, -remaining)

            elapsed += slots_used

            if max_heap:
                elapsed += (n + 1) - slots_used

        return elapsed


if __name__ == "__main__":
    solution = Solution()
    print(solution.leastInterval(["A", "A", "A", "B", "B", "B"], 2))
