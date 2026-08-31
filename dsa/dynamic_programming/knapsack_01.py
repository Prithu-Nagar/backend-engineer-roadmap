"""
0/1 Knapsack

Given item weights and values, select each item at most once while
maximizing total value without exceeding the capacity.

Time Complexity:
O(n * capacity)

Space Complexity:
O(capacity)
"""


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")

    if capacity <= 0 or not weights:
        return 0

    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        if weight <= 0:
            raise ValueError("weights must be positive")

        for current_capacity in range(capacity, weight - 1, -1):
            dp[current_capacity] = max(
                dp[current_capacity],
                dp[current_capacity - weight] + value,
            )

    return dp[capacity]


if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    print(knapsack_01(weights, values, 5))
