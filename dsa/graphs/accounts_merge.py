"""
Problem:
Accounts Merge

Pattern:
Graph / Union-Find / connected components

Time Complexity:
O(N * alpha(N) + E log E), where E is the total number of emails.

Space Complexity:
O(N + E)
"""

from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        parent = list(range(len(accounts)))
        size = [1] * len(accounts)
        email_owner: dict[str, int] = {}

        def find(node: int) -> int:
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(first: int, second: int) -> None:
            root_first = find(first)
            root_second = find(second)
            if root_first == root_second:
                return

            if size[root_first] < size[root_second]:
                root_first, root_second = root_second, root_first

            parent[root_second] = root_first
            size[root_first] += size[root_second]

        for index, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_owner:
                    union(index, email_owner[email])
                else:
                    email_owner[email] = index

        merged_emails: dict[int, list[str]] = defaultdict(list)
        for email, owner in email_owner.items():
            merged_emails[find(owner)].append(email)

        result = []
        for owner, emails in merged_emails.items():
            result.append([accounts[owner][0], *sorted(emails)])

        return result
