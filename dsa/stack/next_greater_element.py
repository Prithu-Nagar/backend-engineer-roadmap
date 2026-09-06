"""
LeetCode: Next Greater Element I

Pattern:
Monotonic decreasing stack + hash map

Time Complexity:
O(N + M)

Space Complexity:
O(N + M)
"""

from typing import List


class Solution:
    def nextGreaterElement(
        self,
        nums1: List[int],
        nums2: List[int],
    ) -> List[int]:
        next_greater: dict[int, int] = {}
        stack: list[int] = []

        for value in nums2:
            while stack and stack[-1] < value:
                next_greater[stack.pop()] = value
            stack.append(value)

        return [next_greater.get(value, -1) for value in nums1]


if __name__ == "__main__":
    solution = Solution()
    print(solution.nextGreaterElement([4, 1, 2], [1, 3, 4, 2]))
    print(solution.nextGreaterElement([2, 4], [1, 2, 3, 4]))
