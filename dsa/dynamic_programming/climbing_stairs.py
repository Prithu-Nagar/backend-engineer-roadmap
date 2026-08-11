"""
LeetCode 70 - Climbing Stairs

Topic:
Dynamic Programming - 1D DP
"""

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        previous = 1
        current = 1

        for _ in range(2, n + 1):
            previous, current = current, previous + current

        return current

if __name__ == "__main__":
    solution = Solution()

    print(solution.climbStairs(2))
    print(solution.climbStairs(5))
