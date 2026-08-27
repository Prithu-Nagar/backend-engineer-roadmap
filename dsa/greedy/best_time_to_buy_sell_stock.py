"""
LeetCode: Best Time to Buy and Sell Stock

Pattern:
Greedy / running minimum

Time Complexity:
O(N)

Space Complexity:
O(1)
"""


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        """Return the maximum profit from one buy and one later sell."""
        if not prices:
            return 0

        minimum_price = prices[0]
        maximum_profit = 0

        for price in prices[1:]:
            maximum_profit = max(maximum_profit, price - minimum_price)
            minimum_price = min(minimum_price, price)

        return maximum_profit
