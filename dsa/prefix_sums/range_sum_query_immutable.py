"""
LeetCode: Range Sum Query - Immutable

Pattern:
Prefix Sum

Time Complexity:
- Construction: O(n)
- Each range query: O(1)

Space Complexity:
O(n)
"""


class NumArray:
    def __init__(self, nums: list[int]):
        """Precompute cumulative sums for constant-time range queries."""
        self.prefix = [0]

        for value in nums:
            self.prefix.append(self.prefix[-1] + value)

    def sumRange(self, left: int, right: int) -> int:
        """Return the inclusive sum from left through right."""
        return self.prefix[right + 1] - self.prefix[left]
