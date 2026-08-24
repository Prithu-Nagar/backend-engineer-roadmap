"""
Problem:
Alien Dictionary

Pattern:
Graph / Topological sort / cycle detection

Time Complexity:
O(C), where C is the total number of characters across all words.

Space Complexity:
O(U + E), where U is the number of unique characters and E is the number
of precedence relationships.
"""

from collections import deque


class Solution:
    def alienOrder(self, words: list[str]) -> str:
        graph = {char: set() for word in words for char in word}
        indegree = {char: 0 for char in graph}

        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""

            for left, right in zip(first, second):
                if left != right:
                    if right not in graph[left]:
                        graph[left].add(right)
                        indegree[right] += 1
                    break

        queue = deque(char for char in indegree if indegree[char] == 0)
        order = []

        while queue:
            char = queue.popleft()
            order.append(char)

            for neighbor in graph[char]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return "".join(order) if len(order) == len(graph) else ""
