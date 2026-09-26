# Binary Search

This directory contains Binary Search implementations and interview problems.

---

## Concepts Covered

- Binary Search
- Iterative Binary Search
- Lower Bound
- Upper Bound
- Binary Search Patterns

---

## Problems

- Binary Search
- Search Insert Position
- Guess Number Higher or Lower

---

## Time Complexity

**Search:** O(log n)

---

## Space Complexity

- Iterative: O(1)
- Recursive: O(log n)

---

## Common Interview Topics

- Binary Search
- Lower Bound
- Upper Bound
- Search Space Reduction
- Binary Search on Answer

---

## Day 28 — Binary Search on Answer

Day 28 applies binary search to a monotonic answer space rather than directly
searching for an element in a sorted array.

### Pattern

- Define the minimum and maximum feasible answer.
- Test a candidate answer.
- Use the monotonic feasibility condition to discard half of the search space.
- Continue until the smallest feasible answer remains.

### Problems

- Koko Eating Bananas
- Capacity To Ship Packages Within D Days

### Implementations

- `koko_eating_bananas.py`
- `capacity_to_ship_packages.py`

### Complexity Pattern

If the answer range is `M` and each feasibility check scans `N` items:

- Time: `O(N log M)`
- Space: `O(1)`

Binary search on answer is especially useful when the problem asks for a
minimum or maximum value subject to a monotonic feasibility condition.

---

## Day 57 — Advanced Search Boundaries

Day 57 extends binary search beyond a simple sorted-array lookup.

### Problems

- Find Minimum in Rotated Sorted Array
- Time Based Key-Value Store
- Search a 2D Matrix II

### Implementations

- `find_minimum_in_rotated_sorted_array.py`
- `time_based_key_value_store.py`
- `search_a_2d_matrix_ii.py`

### Patterns

- Compare the middle element with the right boundary.
- Search for the first or last valid timestamp.
- Use monotonic row and column boundaries to eliminate matrix regions.

### Complexity

For rotated-array minimum:

- Time: `O(log n)`
- Space: `O(1)`

For timestamp lookup with `n` stored versions:

- `set`: `O(1)` amortized when timestamps are appended in order
- `get`: `O(log n)`
- Space: `O(n)`

For an `m x n` sorted matrix using the top-right search:

- Time: `O(m + n)`
- Space: `O(1)`
