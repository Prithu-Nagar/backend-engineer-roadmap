# Data Structures & Algorithms

This directory contains implementations of Data Structures and Algorithms along with LeetCode problems used to strengthen problem-solving and interview preparation.

The implementations focus on understanding the underlying data structure, applying it to common problems, and analyzing time and space complexity.

---

## Topics

### Arrays

Covers array manipulation, searching, hashing-based techniques, and common array interview patterns.

Directory: `arrays/`

### Strings

Covers string traversal, comparison, manipulation, and common string problem-solving patterns.

Directory: `strings/`

### Linked List

Covers singly linked lists, traversal, insertion, deletion, reversal, and common linked-list problems.

Directory: `linked_list/`

### Stack

Covers stack-based problem solving and applications of LIFO behavior.

Directory: `stack/`

### Queue

Covers queue-based problem solving and FIFO behavior.

Directory: `queue/`

### Binary Search

Covers binary search and its applications on sorted data.

Directory: `binary_search/`

### Binary Trees

Covers binary tree traversal and common binary tree problems.

Directory: `binary_tree/`

### Binary Search Trees

Covers BST properties, searching, validation, traversal, and common BST problems.

Directory: `binary_search_tree/`

### Heap

Covers heap-based problem solving using Python's `heapq` module.

Topics include:

- Min Heap
- Max Heap
- Heap construction
- Heap insertion and removal
- Maintaining top K elements
- Priority queue concepts
- Two-heap approach for median finding
- Merging sorted sequences

Day 15 adds advanced heap problems:

- K Closest Points to Origin
- Merge K Sorted Lists
- Find Median from Data Stream

Directory: `heap/`

### Sorting

Covers comparison-based sorting algorithms and sorting-oriented interview problems.

Topics include:

- Merge sort
- Quicksort
- Partitioning
- Stable vs unstable sorting

Directory: `sorting/`

### Graphs

Covers graph traversal, connected components, cloning, and cycle detection.

Topics include:

- DFS/BFS traversal
- Connected components
- Graph cloning
- Topological sort
- Cycle detection
- Flood fill
- Rotting oranges

Directory: `graphs/`

---

## Dynamic Programming

Day 11 introduced Dynamic Programming with a focus on common 1D DP patterns.

Day 12 expands Dynamic Programming into 2D DP and grid-based state formulation.

Topics covered:

- Dynamic Programming fundamentals
- DP state
- Recurrence relations
- Base cases
- Memoization
- Tabulation
- Space optimization
- 1D Dynamic Programming
- 2D Dynamic Programming
- Grid-based Dynamic Programming
- State formulation

Problems covered:

- Climbing Stairs
- House Robber
- Min Cost Climbing Stairs
- Unique Paths
- Minimum Path Sum
- Longest Common Subsequence

The goal is to recognize how a problem can be represented using previous states and to extend that reasoning from one-dimensional sequences to two-dimensional grids and state tables.

Directory: `dynamic_programming/`

---

# Repository Structure

```text
dsa/
├── README.md
├── arrays/
├── strings/
├── linked_list/
├── stack/
├── queue/
├── binary_search/
├── binary_tree/
│   ├── maximum_depth.py
│   ├── invert_binary_tree.py
│   ├── same_tree.py
│   └── binary_tree_level_order_traversal.py
├── binary_search_tree/
├── heap/
├── graphs/
│   ├── number_of_islands.py
│   ├── clone_graph.py
│   ├── course_schedule.py
│   ├── flood_fill.py
│   └── rotting_oranges.py
├── dynamic_programming/
└── hashing/
```

---

### Hashing

Covers hash-based problem solving using dictionaries and sets.

Topics include:

- Frequency maps
- Set membership
- Duplicate detection
- Hash collision intuition
- Prefix sum + hash map patterns

Directory: `hashing/`

---

# LeetCode Problems

DSA implementations are primarily focused on interview-oriented LeetCode problems.

Each topic contains solutions organized by data structure or algorithm.

The corresponding problem list is maintained in:

`leetcode/README.md`

---

### Sliding Window

Covers fixed-size and variable-size sliding window techniques for efficient processing of contiguous subarrays and substrings.

Topics include:

- Fixed-size Sliding Window
- Variable-size Sliding Window
- Two-pointer window movement
- Window expansion and shrinking
- Sliding Window with Set
- Sliding Window with HashMap

Directory: `sliding_window/`

---

### Two Pointers

Day 18 introduces the Two Pointers technique.

Topics include:

- Opposite-direction pointers
- Same-direction pointers
- Pair searching
- Sorted-array techniques
- In-place array processing
- Pointer movement based on conditions

Problems covered:

- Two Sum II
- 3Sum
- Container With Most Water

Directory: `two_pointers/`

### Intervals

Day 19 introduces interval-based problem solving.

Topics include:

- Sorting intervals
- Detecting overlap
- Merging intervals
- Inserting intervals
- Greedy interval selection

Problems covered:

- Merge Intervals
- Insert Interval
- Non-overlapping Intervals

Directory: `intervals/`

---

# Complexity Analysis

Solutions should include consideration of:

- Time Complexity
- Space Complexity
- Input constraints
- Trade-offs between different approaches

The goal is not only to produce a working solution but also to understand its performance characteristics.

---

# Completed Topics

- Arrays
- Strings
- Linked List
- Stack
- Queue
- Binary Search
- Binary Trees
- Binary Search Trees
- Heap
- Graphs
- Dynamic Programming
- Hashing
- Sliding Window
- Two Pointers

---

# Upcoming Topics

- Backtracking
- Advanced Tree Algorithms
- Advanced Graph Algorithms

---

# Learning Approach

For each DSA topic:

1. Understand the underlying data structure or algorithm.
2. Study common patterns and operations.
3. Implement solutions in Python.
4. Solve representative interview problems.
5. Analyze time and space complexity.
6. Review alternative approaches where appropriate.

---

## Day 23 — Binary Search Trees

Day 23 extends BST problem solving using the ordering property and inorder
traversal.

Problems covered:

- Lowest Common Ancestor of a BST
- Kth Smallest Element in a BST

Directory: `binary_search_tree/`

---

## Day 24 — Graphs: Topological Sort

Day 24 introduces topological sorting for dependency graphs.

Topics include:

- Directed graphs
- Indegree
- Kahn's algorithm
- Cycle detection
- Dependency ordering

Problems:

- Course Schedule II
- Alien Dictionary

---

## Day 25 — Graphs: Union-Find / DSU

Day 25 introduces Disjoint Set Union for connectivity and cycle-detection
problems.

Topics:

- Parent arrays
- Path compression
- Union by size
- Connected components
- Cycle detection

Problems:

- Number of Provinces
- Redundant Connection
- Accounts Merge

Directory: `graphs/`

---

## Day 26 — Sorting

Day 26 introduces comparison-based sorting through merge sort and quicksort.

Topics:

- Divide-and-conquer sorting
- Merge sort
- Quicksort
- Partitioning
- Stable vs unstable sorting
- Best, average, and worst-case complexity

Implementations:

- `sorting/merge_sort.py`
- `sorting/quick_sort.py`
- `sorting/sort_array.py` — LeetCode: Sort an Array

---

## Day 27 — Greedy Algorithms

Day 27 introduces greedy problem solving and focuses on identifying situations
where a locally optimal choice can lead to a globally optimal result.

Topics:

- Greedy-choice reasoning
- Running best-so-far state
- Reachability tracking
- Running balance
- Proving or validating a greedy strategy

Implementations:

- `greedy/best_time_to_buy_sell_stock.py`
- `greedy/jump_game.py`
- `greedy/gas_station.py`

---

## Day 28 — Binary Search on Answer

Day 28 applies binary search to a monotonic answer space rather than directly
searching for a value in a sorted array.

Topics:

- Defining a feasible answer range
- Monotonic feasibility checks
- Minimum feasible answer
- Binary search on answer

Problems:

- Koko Eating Bananas
- Capacity To Ship Packages Within D Days

Implementations are stored in `binary_search/`.

---

## Day 29 — Prefix Sums / Difference Arrays

Day 29 introduces prefix sums and difference arrays for efficient repeated
queries and range updates.

Topics:

- Prefix sums
- Range-sum queries
- Prefix/suffix products
- Difference arrays
- Boundary updates
- Efficient preprocessing

Problems:

- Product of Array Except Self
- Range Sum Query - Immutable

Implementations are stored in `prefix_sums/`.
