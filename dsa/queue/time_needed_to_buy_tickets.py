"""
LeetCode 2073
Time Needed to Buy Tickets

Time Complexity
---------------
O(n)

Space Complexity
----------------
O(1)
"""


class Solution:

    def timeRequiredToBuy(self, tickets, k):

        time = 0

        for i in range(len(tickets)):

            if i <= k:
                time += min(tickets[i], tickets[k])
            else:
                time += min(tickets[i], tickets[k] - 1)

        return time