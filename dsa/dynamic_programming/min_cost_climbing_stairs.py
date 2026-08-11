"""
LeetCode 746 - Min Cost Climbing Stairs

Topic:
Dynamic Programming - 1D DP
"""

class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        previous = cost[0]
        current = cost[1]

        for i in range(2, len(cost)):
            next_cost = cost[i] + min(previous, current)
            previous = current
            current = next_cost

        return min(previous, current)

if __name__ == "__main__":
    solution = Solution()
    print(solution.minCostClimbingStairs([10, 15, 20]))
    print(
        solution.minCostClimbingStairs(
            [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
        )
    )
