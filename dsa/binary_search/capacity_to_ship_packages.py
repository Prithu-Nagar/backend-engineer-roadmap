"""
LeetCode: Capacity To Ship Packages Within D Days

Pattern:
Binary Search on Answer

Time Complexity:
O(N log S)

Space Complexity:
O(1)

Where:
- N is the number of packages.
- S is the search range between the largest package and total weight.
"""


class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        """Return the minimum ship capacity needed within the given days."""
        left = max(weights)
        right = sum(weights)

        while left < right:
            capacity = left + (right - left) // 2

            days_needed = 1
            current_load = 0

            for weight in weights:
                if current_load + weight > capacity:
                    days_needed += 1
                    current_load = 0

                current_load += weight

            if days_needed <= days:
                right = capacity
            else:
                left = capacity + 1

        return left
