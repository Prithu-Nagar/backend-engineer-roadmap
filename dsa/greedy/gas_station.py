"""
LeetCode: Gas Station

Pattern:
Greedy / running balance

Time Complexity:
O(N)

Space Complexity:
O(1)
"""


class Solution:
    def canCompleteCircuit(
        self,
        gas: list[int],
        cost: list[int],
    ) -> int:
        """Return a valid starting station, or -1 when none exists."""
        if len(gas) != len(cost) or not gas:
            return -1

        total_balance = 0
        current_balance = 0
        start = 0

        for index, (gas_amount, travel_cost) in enumerate(zip(gas, cost)):
            balance = gas_amount - travel_cost
            total_balance += balance
            current_balance += balance

            if current_balance < 0:
                start = index + 1
                current_balance = 0

        return start if total_balance >= 0 else -1
