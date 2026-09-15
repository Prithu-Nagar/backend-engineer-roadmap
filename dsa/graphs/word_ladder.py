"""Day 46 — Word Ladder.

Interview pattern: BFS over an implicit unweighted graph of one-letter
transformations.
"""

from __future__ import annotations

from collections import defaultdict, deque


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """Return the shortest transformation sequence length, or 0 if absent."""
    words = set(word_list)
    if end_word not in words:
        return 0

    patterns: dict[str, list[str]] = defaultdict(list)
    for word in words | {begin_word}:
        for index in range(len(word)):
            pattern = word[:index] + "*" + word[index + 1 :]
            patterns[pattern].append(word)

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, distance = queue.popleft()
        if word == end_word:
            return distance

        for index in range(len(word)):
            pattern = word[:index] + "*" + word[index + 1 :]
            for neighbor in patterns[pattern]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
            patterns[pattern].clear()

    return 0
