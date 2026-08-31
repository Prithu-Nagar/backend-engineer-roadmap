# LeetCode

This directory tracks the LeetCode problems solved throughout the Backend Engineer Roadmap.

The purpose is to strengthen problem-solving skills, recognize common DSA patterns, and prepare for backend engineering interviews.

Solutions are organized according to the DSA topics being studied in the roadmap.

---

# Problem Progress

## Day 1 — Arrays & Hashing

- Two Sum
- Contains Duplicate
- Valid Anagram

---

## Day 2 — Strings

- Valid Palindrome
- Reverse String
- Is Subsequence

---

## Day 3 — Linked List

- Reverse Linked List
- Merge Two Sorted Lists
- Linked List Cycle

---

## Day 4 — Stack

- Valid Parentheses
- Min Stack
- Baseball Game

---

## Day 5 — Queue

- Implement Queue using Stacks
- Number of Recent Calls
- Time Needed to Buy Tickets

---

## Day 6 — Binary Search

- Binary Search
- Search Insert Position
- Guess Number Higher or Lower

---

## Day 7 — Binary Trees

- Maximum Depth of Binary Tree
- Invert Binary Tree
- Same Tree

---

## Day 8 — Binary Search Trees

- Search in a Binary Search Tree
- Validate Binary Search Tree
- Minimum Distance Between BST Nodes

---

## Day 9 — Heap

- Kth Largest Element in an Array
- Top K Frequent Elements
- Last Stone Weight

---

## Day 10 — Graphs

- Number of Islands
- Clone Graph
- Course Schedule

---

## Day 11 — Dynamic Programming

- Climbing Stairs
- House Robber
- Min Cost Climbing Stairs

---

## Day 12 — Dynamic Programming

- Unique Paths
- Minimum Path Sum
- Longest Common Subsequence

---

## Day 13 — Graphs

- Flood Fill
- Rotting Oranges
- Binary Tree Level Order Traversal

---

## Day 14 — Advanced Graph / Shortest Path

- Network Delay Time
- Shortest Path in a Binary Matrix

---

## Day 15 — Heap (Advanced)

- K Closest Points to Origin
- Merge K Sorted Lists
- Find Median from Data Stream

---

## Day 16 — Hashing

- Group Anagrams
- Longest Consecutive Sequence
- Subarray Sum Equals K

---

## Day 17 — Sliding Window

- Longest Substring Without Repeating Characters
- Minimum Size Subarray Sum
- Permutation in String

---

## Day 18 - Two Pointers

- Two Sum II - Input Array Is Sorted
- 3Sum
- Container With Most Water

---

## Day 19 — Intervals

- Merge Intervals
- Insert Interval
- Non-overlapping Intervals

---

## Day 20 — Recursion & Backtracking

- Subsets
- Permutations
- Combination Sum

---

## Day 21 — Backtracking

- Letter Combinations of a Phone Number
- Word Search

---

## Day 22 — Binary Trees / DFS

- Diameter of Binary Tree
- Balanced Binary Tree
- Path Sum

---

# Problem-Solving Approach

For each LeetCode problem:

1. Understand the problem statement.
2. Identify the underlying DSA pattern.
3. Determine the appropriate data structure or algorithm.
4. Consider edge cases.
5. Implement the solution.
6. Analyze time complexity.
7. Analyze space complexity.
8. Review alternative approaches when useful.

---

# DSA Pattern Progress

The problems solved so far cover:

- Arrays
- Hashing
- Strings
- Linked Lists
- Stacks
- Queues
- Binary Search
- Binary Trees
- Binary Search Trees
- Heaps
- Graphs
- Dynamic Programming
- Intervals

Dynamic Programming currently includes:

- 1D DP
- 2D DP
- Grid DP
- Sequence-based DP
- Space optimization

---

# Organization

LeetCode solutions are stored under the relevant DSA directories.

For example:

dsa/
```text
├── arrays/
├── strings/
├── linked_list/
├── stack/
├── queue/
├── binary_search/
├── binary_tree/
├── binary_search_tree/
├── heap/
├── graphs/
└── dynamic_programming/
```

The leetcode/ directory serves as the progress tracker, while the actual implementations are maintained under dsa/.

Future Problems

Future LeetCode problems will be added as new DSA topics are introduced in the roadmap.

Upcoming areas include:

Backtracking
Advanced Trees
Advanced Graph Algorithms
More Dynamic Programming patterns

---

## Day 23 — Binary Search Trees

- Lowest Common Ancestor of a BST
- Kth Smallest Element in a BST

---

## Day 24 — Topological Sort

- Course Schedule II
- Alien Dictionary


## Day 25 — Union-Find / DSU

- Number of Provinces
- Redundant Connection
- Accounts Merge

---

## Day 26 — Sorting

- Sort an Array
- Kth Largest Element in an Array — revision

The Sort an Array implementation is stored in `dsa/sorting/sort_array.py`. The
Kth Largest problem is revisited using the existing heap implementation in
`dsa/heap/kth_largest_element.py`.

---

## Day 27 — Greedy Algorithms

- Best Time to Buy and Sell Stock
- Jump Game
- Gas Station

The implementations are stored in `dsa/greedy/`.

---

## Day 28 — Binary Search on Answer

- Koko Eating Bananas
- Capacity To Ship Packages Within D Days

The implementations are stored in `dsa/binary_search/`.

---

## Day 29 — Prefix Sums / Prefix-Suffix Pattern

- Product of Array Except Self
- Range Sum Query - Immutable

The implementations are stored in `dsa/prefix_sums/`.

---

## Day 30 — Mixed Timed Set

Day 30 uses a mixed timed set to review patterns from Days 11–29.

Recommended timed set:

1. **House Robber** — Dynamic Programming
2. **Course Schedule II** — Graphs / Topological Sort
3. **Kth Largest Element in an Array** — Heap
4. **Koko Eating Bananas** — Binary Search on Answer
5. **Product of Array Except Self** — Prefix/Suffix

The set intentionally mixes previously covered patterns rather than introducing
new problem types. Use the existing implementations under `dsa/` after the
timed attempt for review and comparison.

## Day 31 — Advanced Dynamic Programming

- Partition Equal Subset Sum
- Coin Change

Both problems are implemented under `dsa/dynamic_programming/` and reinforce
the knapsack/subset-sum family of Dynamic Programming patterns.
