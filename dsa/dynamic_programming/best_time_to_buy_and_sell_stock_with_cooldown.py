"""
LeetCode 309
Best Time to Buy and Sell Stock with Cooldown

Time Complexity:
O(n)

Space Complexity:
O(1)
"""


def max_profit(prices: list[int]) -> int:
    """Return the maximum profit with a one-day cooldown after selling."""
    if not prices:
        return 0

    holding = -prices[0]
    sold = 0
    resting = 0

    for price in prices[1:]:
        previous_holding = holding
        previous_sold = sold
        previous_resting = resting

        holding = max(previous_holding, previous_resting - price)
        sold = previous_holding + price
        resting = max(previous_resting, previous_sold)

    return max(sold, resting)


if __name__ == "__main__":
    print(max_profit([1, 2, 3, 0, 2]))
    print(max_profit([1]))
