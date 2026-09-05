"""
LeetCode: Design Add and Search Words Data Structure

Pattern:
Trie + DFS backtracking for wildcard search

Time Complexity:
O(L) for addWord.
search() is O(L) for a normal word and can branch across children for '.'
wildcards. In the worst case, wildcard-heavy searches can visit many trie
nodes.

Space Complexity:
O(T), where T is the total number of stored characters.
"""

from __future__ import annotations


class TrieNode:
    """Node used by the word dictionary trie."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root

        for character in word:
            node = node.children.setdefault(character, TrieNode())

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        return self._search_from(self.root, word, 0)

    def _search_from(self, node: TrieNode, word: str, index: int) -> bool:
        if index == len(word):
            return node.is_end_of_word

        character = word[index]

        if character != ".":
            child = node.children.get(character)
            return child is not None and self._search_from(child, word, index + 1)

        return any(
            self._search_from(child, word, index + 1)
            for child in node.children.values()
        )
