# Data Structures & Algorithms

This directory contains Data Structures and Algorithms concepts along with LeetCode solutions implemented throughout the Backend Engineer Roadmap.

The goal is to build strong problem-solving skills and develop the ability to identify common interview patterns.

---

## Completed Topics

- Arrays
- Strings
- Linked List
- Stack
- Queue
- Binary Search
- Binary Trees

---

## Upcoming Topics

- Binary Search Tree
- Heap
- Graph
- Dynamic Programming
- Backtracking
- Advanced Tree Algorithms
- Advanced Graph Algorithms

---

# Repository Structure

dsa/
├── README.md
├── arrays/
├── strings/
├── linked_list/
├── stack/
├── queue/
├── binary_search/
└── binary_tree/

---

# Topics

## Arrays

Covers fundamental array and hashing-based problems.

Topics include:

* Array traversal
* Hashing
* Duplicate detection
* Two-pointer fundamentals

**Directory:** `arrays/`

---

## Strings

Covers common string manipulation and two-pointer techniques.

Topics include:

* String traversal
* Palindrome checking
* Subsequence checking
* String reversal

**Directory:** `strings/`

---

## Linked List

Covers fundamental linked-list operations and pointer manipulation.

Topics include:

* Traversal
* Reversal
* Merging lists
* Cycle detection

**Directory:** `linked_list/`

---

## Stack

Covers stack-based problem-solving patterns.

Topics include:

* Parentheses validation
* Min Stack
* Stack simulation
* Expression/state tracking

**Directory:** `stack/`

---

## Queue

Covers queue-based data structures and problems.

Topics include:

* Queue operations
* Circular queues
* Queue simulation
* Stack using queues

**Directory:** `queue/`

---

## Binary Search

Binary Search efficiently searches a sorted search space.

The general pattern is:

left
  ↓
[mid]
  ↓
right

At each step, the search space is reduced approximately by half.

**Directory:** `binary_search/`

---

## Binary Trees

Binary Trees contain nodes with at most two children.

Common recursive problems follow the pattern:

if root is None:
    return base_case

left = solve(root.left)
right = solve(root.right)

return combine(left, right)

Topics covered include:

* Tree height
* Tree comparison
* Tree inversion
* DFS
* Recursive tree traversal

**Directory:** `binary_tree/`

---

# Learning Progress

| Topic               | Status    |
| ------------------- | --------- |
| Arrays              | Completed |
| Strings             | Completed |
| Linked List         | Completed |
| Stack               | Completed |
| Queue               | Completed |
| Binary Search       | Completed |
| Binary Trees        | Completed |
| Binary Search Tree  | Upcoming  |
| Heap                | Upcoming  |
| Graph               | Upcoming  |
| Dynamic Programming | Upcoming  |

---

# Problem-Solving Strategy

For every DSA problem:

1. Understand the problem.
2. Identify the data structure.
3. Identify the underlying pattern.
4. Consider a brute-force approach.
5. Optimize the solution.
6. Implement the solution cleanly.
7. Analyze time complexity.
8. Analyze space complexity.
9. Record the key insight for revision.

The goal is to develop pattern-recognition skills that can be applied to new interview problems.
