"""
LeetCode: Meeting Rooms II

Pattern:
Greedy interval processing with a min-heap of active meeting end times.

Time Complexity:
O(n log n)

Space Complexity:
O(n)
"""

from __future__ import annotations

import heapq


class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0

        intervals.sort(key=lambda interval: interval[0])
        end_times: list[int] = []

        for start, end in intervals:
            if end_times and end_times[0] <= start:
                heapq.heappop(end_times)

            heapq.heappush(end_times, end)

        return len(end_times)


if __name__ == "__main__":
    solution = Solution()
    print(solution.minMeetingRooms([[0, 30], [5, 10], [15, 20]]))
