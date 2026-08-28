"""
LeetCode: Koko Eating Bananas

Pattern:
Binary Search on Answer

Time Complexity:
O(N log M)

Space Complexity:
O(1)

Where:
- N is the number of piles.
- M is the maximum pile size.
"""


class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        """Return the minimum eating speed that finishes within h hours."""
        left = 1
        right = max(piles)

        while left < right:
            speed = left + (right - left) // 2
            hours_needed = sum(
                (pile + speed - 1) // speed
                for pile in piles
            )

            if hours_needed <= h:
                right = speed
            else:
                left = speed + 1

        return left
