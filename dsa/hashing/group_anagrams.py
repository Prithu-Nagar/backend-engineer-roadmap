"""
LeetCode 49 - Group Anagrams
"""

from collections import defaultdict


def group_anagrams(strs):
    groups = defaultdict(list)

    for word in strs:
        frequency = [0] * 26

        for char in word:
            frequency[ord(char) - ord("a")] += 1

        groups[tuple(frequency)].append(word)

    return list(groups.values())


if __name__ == "__main__":
    print(
        group_anagrams(
            ["eat", "tea", "tan", "ate", "nat", "bat"]
        )
    )