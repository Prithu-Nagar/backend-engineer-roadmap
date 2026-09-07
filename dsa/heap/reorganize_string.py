"""
LeetCode: Reorganize String

Pattern:
Max-heap + greedy placement of the most frequent character while preventing
adjacent equal characters.

Time Complexity:
O(N log K), where K is the number of distinct characters.

Space Complexity:
O(K)
"""

from __future__ import annotations

from collections import Counter
import heapq


class Solution:
    def reorganizeString(self, s: str) -> str:
        frequencies = Counter(s)
        max_heap = [(-count, character) for character, count in frequencies.items()]
        heapq.heapify(max_heap)

        result: list[str] = []
        previous_count = 0
        previous_character = ""

        while max_heap:
            count, character = heapq.heappop(max_heap)

            result.append(character)
            count += 1

            if previous_count < 0:
                heapq.heappush(max_heap, (previous_count, previous_character))

            previous_count = count
            previous_character = character

        if previous_count < 0:
            return ""

        return "".join(result)


if __name__ == "__main__":
    solution = Solution()
    print(solution.reorganizeString("aab"))
