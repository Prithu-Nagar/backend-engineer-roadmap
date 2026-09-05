# Trie

This directory contains trie-based data structures and interview problems.

---

## Concepts Covered

- Prefix trees
- Character-by-character traversal
- Exact word lookup
- Prefix lookup
- Trie node design
- Wildcard search
- DFS backtracking over trie branches

---

## Problems Solved

- Implement Trie (Prefix Tree)
- Design Add and Search Words Data Structure

---

## Files

- `trie.py` — reusable Trie implementation
- `implement_trie.py` — LeetCode: Implement Trie (Prefix Tree)
- `add_and_search_words.py` — LeetCode: Design Add and Search Words Data Structure

---

## Complexity

For a word of length `L`:

- Insert: `O(L)`
- Exact search: `O(L)`
- Prefix search: `O(L)`

A wildcard search can branch across multiple children, so its worst-case
runtime depends on the number of matching trie paths.

---

## Day 36 — Trie

Day 36 introduces the Trie data structure for efficient prefix-based string
operations.

Topics include:

- Trie nodes
- Character transitions
- Exact word lookup
- Prefix lookup
- Wildcard matching with DFS
