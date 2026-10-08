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

## Future Problems

Future LeetCode problems will be added as new DSA topics are introduced in the roadmap.

Upcoming areas include:

- Backtracking
- Advanced Trees
- Advanced Graph Algorithms
- More Dynamic Programming patterns

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

---

## Day 31 — Advanced Dynamic Programming

- Partition Equal Subset Sum
- Coin Change

Both problems are implemented under `dsa/dynamic_programming/` and reinforce
the knapsack/subset-sum family of Dynamic Programming patterns.

---

## Day 32 — Advanced Dynamic Programming

- Longest Increasing Subsequence
- Decode Ways

Both problems are implemented under `dsa/dynamic_programming/`.

---

## Day 33 — Dynamic Programming: State Reduction

- Unique Paths II
- House Robber II

Both problems are implemented under `dsa/dynamic_programming/` and reinforce
state compression and the reduction of circular constraints to linear DP cases.

---

## Day 34 — Graph Shortest Paths

- Network Delay Time
- Cheapest Flights Within K Stops

The problems reinforce Dijkstra-style shortest-path reasoning and the use of
an explicit stop-count state when the path length is bounded.

Implementations are stored in `dsa/graphs/`.

---

## Day 35 — Minimum Spanning Tree

- Min Cost to Connect All Points

The problem reinforces Kruskal's algorithm, Union-Find, edge sorting, and
minimum spanning tree construction. The implementation is stored in
`dsa/graphs/`.

---

## Day 36 — Trie

- Implement Trie (Prefix Tree)
- Design Add and Search Words Data Structure

The implementations are stored in `dsa/trie/`.

---

## Day 37 — Monotonic Stack

- Daily Temperatures
- Next Greater Element I

Both problems are implemented under `dsa/stack/` and reinforce the monotonic
stack pattern for resolving next-greater relationships in linear time.

---

## Day 38 — Heap + Greedy

- Task Scheduler
- Reorganize String

Both problems combine heap-based priority selection with greedy decisions and
are implemented under `dsa/heap/`.

---

## Day 39 — Mixed Medium Review

- Binary Tree Level Order Traversal
- Number of Islands
- Coin Change

The set intentionally mixes tree, graph, and Dynamic Programming patterns. The
existing implementations under `dsa/binary_tree/`, `dsa/graphs/`, and
`dsa/dynamic_programming/` are used for review after the timed attempt.

---

## Day 40 — Timed Mixed Set

Day 40 uses a timed mixed set to consolidate patterns covered during the
Databases & Distributed Systems phase and earlier DSA foundations.

Recommended assessment set:

1. **Binary Tree Level Order Traversal** — Trees / BFS
2. **Number of Islands** — Graphs / BFS-DFS
3. **Coin Change** — Dynamic Programming
4. **Task Scheduler** — Heap / Greedy
5. **Daily Temperatures** — Monotonic Stack

Use the existing implementations under `dsa/` only after the timed attempt for
comparison, complexity analysis, and targeted revision.

---

## Day 41 — Advanced Weighted Graphs

- Path With Minimum Effort
- Swim in Rising Water

Both problems reinforce Dijkstra-style reasoning where the path cost is the
maximum edge or cell cost encountered along the route.

---

## Day 44 — Binary Search & Intervals Review

Recommended pattern set:

- Search in Rotated Sorted Array
- Find First and Last Position of Element in Sorted Array
- Interval List Intersections

Use the corresponding implementations under `dsa/binary_search/` and
`dsa/intervals/` after attempting the problems without looking at the solution.

---

## Day 45 — Hashing & Prefix Sums Review

Recommended pattern set:

- Subarray Sum Equals K
- Contiguous Array
- Subarray Sums Divisible by K

The set reinforces prefix-state counting, balance tracking, remainder
normalization, and O(n) hash-map based subarray counting.

---

## Day 46 — Tree / Graph Interview Patterns

Recommended medium-level pattern set:

- Lowest Common Ancestor of a Binary Tree
- Binary Tree Right Side View
- Word Ladder

Attempt each problem independently before comparing against the implementations
under `dsa/binary_tree/` and `dsa/graphs/`.

---

## Day 47 — Backtracking Review

- N-Queens
- Combination Sum II
- Palindrome Partitioning

The implementations are stored under `dsa/recursion/` and reinforce constraint
tracking, duplicate pruning, recursive state, and state restoration.

---

## Day 48 — Heap / Greedy Review

Recommended pattern set:

- IPO
- Furthest Building You Can Reach
- Maximum Performance of a Team

Attempt each problem independently before comparing against the implementations
under `dsa/heap/`.

The set reinforces heap-based candidate selection, greedy exchanges, sorting by
the active constraint, and maintaining an optimal bounded set of choices.

---

## Day 49 — Full Mixed Timed Set

Recommended four-problem mixed set:

1. **Maximum Subarray** — Arrays / Dynamic Programming
2. **Longest Palindromic Substring** — Strings / Two-ended expansion
3. **Binary Tree Zigzag Level Order Traversal** — Trees / BFS
4. **LRU Cache** — Hash Map + Linked List / Design

Attempt the problems under timed conditions before comparing against the
implementations under `dsa/`.

---

## Day 50 — Timed Assessment

Day 50 uses a timed LeetCode assessment to consolidate the DSA patterns covered
through the first 49 days.

Assessment focus:

- Mixed pattern recognition
- Time and space complexity analysis
- Choosing an approach without a pattern label
- Identifying weak areas from incorrect or incomplete attempts
- Re-attempting weak patterns after the timed session

No new fixed problem list is required for Day 50. Use the assessment to select
problems that reflect the user's weakest patterns and compare against the
existing implementations under `dsa/` only after the timed attempt.

---

## Day 51 — Mixed Interview Set

Recommended three-problem set:

1. **Product of Array Except Self** — Arrays / Prefix-Suffix
2. **Search a 2D Matrix** — Binary Search
3. **Longest Palindromic Subsequence** — Dynamic Programming


---

## Day 52 — Hashing / Sliding Window Pattern Set

Recommended three-problem set:

1. **Minimum Window Substring** — Sliding Window + Frequency Map
2. **Longest Repeating Character Replacement** — Sliding Window + Frequency Map
3. **Subarrays with K Different Integers** — Hashing + Sliding Window

---

## Day 53 — Trees / Graphs

Recommended three-problem set:

1. **Binary Tree Level Order Traversal** — Tree BFS
2. **Number of Islands** — Graph Traversal / DFS
3. **Course Schedule** — Graph / Topological Sort

Attempt the problems under timed conditions before comparing against the
implementations under `dsa/`.

---

## Day 54 — Dynamic Programming

Recommended three-problem set:

1. **Coin Change** — 1D Dynamic Programming
2. **Decode Ways** — 1D Dynamic Programming / State Transitions
3. **Word Break** — Dynamic Programming / Prefix State

Attempt the problems under timed conditions before comparing against the
existing implementations under `dsa/`.

---

## Day 55 — Backtracking

- Restore IP Addresses
- Generate Parentheses
- Combination Sum III

---

## Day 56 — Heap + Greedy

Recommended three-problem set:

1. **Kth Smallest Element in a Sorted Matrix** — Heap / K-way merge
2. **Meeting Rooms II** — Greedy / Min-Heap
3. **Minimum Number of Refueling Stops** — Greedy / Max-Heap

The implementations are stored under `dsa/heap/`.

Attempt the problems independently before comparing against the implementations
and reviewing why the heap maintains the currently useful candidates.

---

## Day 57 — Binary Search / Search

- Find Minimum in Rotated Sorted Array
- Time Based Key-Value Store
- Search a 2D Matrix II

---

## Day 58 — Mixed Medium Set

Recommended three-problem set:

1. **3Sum** — Arrays / Sorting + Two Pointers
2. **Validate Binary Search Tree** — Trees / Recursive Bounds
3. **Pacific Atlantic Water Flow** — Graphs / Reverse Reachability

---

## Day 59 — Mixed Medium Set

Recommended three-problem set:

1. **Maximum Product Subarray** — Arrays / Dynamic Programming
2. **Decode String** — Strings / Stack
3. **Find Peak Element** — Binary Search

---

## Day 60 — Timed Assessment

Day 60 uses a timed LeetCode assessment to consolidate the DSA patterns covered
through the GenAI Engineering phase.

Assessment focus:

- Mixed-pattern recognition
- Selecting an approach without a topic label
- Time and space complexity analysis
- Writing a complete solution under time pressure
- Recording incorrect, incomplete, or slow attempts
- Re-attempting weak patterns after the timed session

No new fixed problem list is required for Day 60. Select a mixed set from the
existing problem patterns and compare against implementations under `dsa/` only
after the timed attempt.

---

## Day 61 — Design-Oriented Problems

Day 61 shifts LeetCode practice toward problems that require explicit state,
object boundaries, and data-structure design.

Review set:

- **LRU Cache** — combine a hash map with a doubly linked list to provide
  constant-time lookup, update, and eviction
- **Design Add and Search Words Data Structure** — encapsulate trie nodes and
  support wildcard-aware recursive search

Both implementations already exist under `dsa/` and are reused rather than
creating duplicate files. The review should focus on API contracts, invariants,
complexity, ownership, and how the implementation could be exposed as a backend
component.

---

## Day 62 — OOP / Graph Review

Day 62 uses two existing medium-level graph problems to practice switching
between algorithmic reasoning and object-design concerns.

Review set:

1. **Clone Graph** — Graph traversal with explicit node ownership and visited-state management
2. **Course Schedule** — Graph cycle detection / topological reasoning

Both implementations already exist under `dsa/graphs/` and are reused rather
than creating duplicate files. Focus on API boundaries, state ownership,
complexity, and how the algorithms could be isolated behind a backend service
interface.

---

## Day 63 — Trees / Recursion

Day 63 uses two existing medium-level tree problems to reinforce recursive
decomposition, traversal state, and correctness invariants.

Review set:

1. **Binary Tree Right Side View** — tree traversal with depth-aware state
2. **Path Sum II** — recursive path tracking and backtracking

Both implementations already exist under `dsa/binary_tree/` and are reused
rather than creating duplicate files. Focus on base cases, traversal order,
state ownership, complexity, and when recursion should be replaced by an
explicit stack.

---

## Day 64 — Graph Connectivity

Day 64 uses two medium-level graph problems to reinforce connectivity and
cycle-detection reasoning.

Problems:

1. **Graph Valid Tree** — Union-Find + edge-count reasoning
2. **Number of Connected Components in an Undirected Graph** — DFS connected components

Both implementations are stored under `dsa/graphs/`.

Attempt the problems independently before comparing against the implementations
and reviewing the graph invariants and complexity.

---

## Day 65 — Dynamic Programming

Day 65 uses two medium-level Dynamic Programming problems.

Problems:

1. **Target Sum** — subset-sum transformation + counting DP
2. **Best Time to Buy and Sell Stock with Cooldown** — state-machine DP

Both implementations are stored under `dsa/dynamic_programming/`.

Focus on defining the state and transition before optimizing space.

---

## Day 66 — Mixed Medium Problems

Day 66 returns to a mixed medium-level set to practice pattern recognition
without being given the topic in advance.

Review set:

1. **Merge Intervals** — sorting and interval merging
2. **Number of Islands** — graph traversal with DFS/BFS

Both implementations already exist under `dsa/` and are reused rather than
creating duplicate solution files. Focus on identifying the pattern, stating
the invariant, and explaining the complexity before comparing against the
existing implementations.

---

## Day 67 — Mixed Medium Problems

Day 67 continues mixed medium-level practice with two existing implementations.

Review set:

1. **Rotting Oranges** — multi-source BFS and level-by-level state propagation
2. **K Closest Points to Origin** — heap-based candidate selection

Both implementations already exist under `dsa/` and are reused rather than
creating duplicate solution files. Focus on recognizing the underlying pattern,
defining the invariant, and comparing complexity before reviewing the code.

---

## Day 68 — Mixed Medium Problems

Day 68 continues mixed medium-level practice with two existing implementations.

Review set:

1. **Longest Consecutive Sequence** — hash-set based sequence detection
2. **Word Break** — dynamic programming over valid prefix states

Both implementations already exist under `dsa/` and are reused rather than
creating duplicate solution files. Focus on pattern recognition, state/invariant
definition, complexity, and explaining why each approach is appropriate.

---

## Day 69 — Mixed Medium Problems

Day 69 continues mixed medium-level practice with two existing implementations.

Review set:

1. **Find Median from Data Stream** — two heaps for online median maintenance
2. **Search in Rotated Sorted Array** — modified binary search on a rotated array

Both implementations already exist under `dsa/` and are reused rather than
creating duplicate solution files. Focus on recognizing the pattern, stating
the invariant, and explaining complexity before reviewing the code.
