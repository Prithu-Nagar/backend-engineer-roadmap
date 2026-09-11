"""LeetCode: Coin Change II

Day 42 — Dynamic Programming mixed review.
"""

from __future__ import annotations


def change(amount: int, coins: list[int]) -> int:
    """Return the number of combinations that make ``amount``."""
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for current in range(coin, amount + 1):
            dp[current] += dp[current - coin]

    return dp[amount]
