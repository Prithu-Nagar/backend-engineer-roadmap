"""
LeetCode 322
Coin Change

Time Complexity:
O(amount * number_of_coins)

Space Complexity:
O(amount)
"""


def coin_change(coins: list[int], amount: int) -> int:
    if amount == 0:
        return 0

    if amount < 0:
        return -1

    if any(coin <= 0 for coin in coins):
        raise ValueError("coin values must be positive")

    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for current_amount in range(1, amount + 1):
        for coin in coins:
            if coin <= current_amount:
                dp[current_amount] = min(
                    dp[current_amount],
                    dp[current_amount - coin] + 1,
                )

    return -1 if dp[amount] == amount + 1 else dp[amount]


if __name__ == "__main__":
    print(coin_change([1, 2, 5], 11))
