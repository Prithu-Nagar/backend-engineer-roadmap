"""
LeetCode: Daily Temperatures

Pattern:
Monotonic decreasing stack of indexes

Time Complexity:
O(N)

Space Complexity:
O(N)
"""

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        result = [0] * len(temperatures)
        stack: list[int] = []

        for index, temperature in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temperature:
                previous = stack.pop()
                result[previous] = index - previous

            stack.append(index)

        return result


if __name__ == "__main__":
    solution = Solution()
    print(solution.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
