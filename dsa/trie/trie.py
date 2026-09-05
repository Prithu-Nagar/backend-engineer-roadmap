"""
Trie / Prefix Tree

Pattern:
Trie for prefix-based string lookup

Time Complexity:
O(L) per insert, search, or prefix query, where L is the word length.

Space Complexity:
O(T), where T is the number of characters stored in the trie.
"""

from __future__ import annotations


class TrieNode:
    """A trie node containing child nodes and a word-end marker."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False


class Trie:
    """Prefix tree supporting insertion, exact search, and prefix search."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root

        for character in word:
            node = node.children.setdefault(character, TrieNode())

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Return True when the complete word exists in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Return True when at least one stored word has the given prefix."""
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> TrieNode | None:
        """Return the node reached by text, or None when the path is absent."""
        node = self.root

        for character in text:
            node = node.children.get(character)
            if node is None:
                return None

        return node


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")

    print(trie.search("apple"))
    print(trie.search("app"))
    print(trie.starts_with("app"))

    trie.insert("app")
    print(trie.search("app"))
