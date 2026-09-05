"""
LeetCode: Implement Trie (Prefix Tree)

Pattern:
Trie / prefix tree

Time Complexity:
O(L) per insert, search, or startsWith operation.

Space Complexity:
O(T), where T is the total number of characters stored.
"""

from __future__ import annotations


class TrieNode:
    """Node used by the prefix tree."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root

        for character in word:
            node = node.children.setdefault(character, TrieNode())

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> TrieNode | None:
        node = self.root

        for character in text:
            node = node.children.get(character)
            if node is None:
                return None

        return node
