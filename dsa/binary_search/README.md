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
