# Two Pointers

The Two Pointers technique uses two indices to traverse a data structure,
usually an array or string, while reducing unnecessary comparisons.

---

## Core Idea

Instead of comparing every possible pair, two pointers allow us to
eliminate unnecessary comparisons by moving one or both pointers based
on the current condition.

Common patterns include:

- Opposite-direction pointers
- Same-direction pointers
- Fast and slow pointers
- Pair searching in sorted arrays
- In-place array manipulation

---

## Opposite-Direction Pattern

A common pattern starts one pointer at the beginning and another at the end.

```python
left = 0
right = len(arr) - 1

while left < right:
    if condition:
        left += 1
    else:
        right -= 1

This is especially useful when the input is sorted or when the problem
requires comparing elements from both ends.

When to Use Two Pointers

Two Pointers is commonly useful when:

The array is sorted.
We need to find a pair satisfying a condition.
We need to compare elements from both ends.
We need an O(n) solution instead of O(n²).
We need to modify an array in-place.
We need to maintain a left and right boundary.
Advantages
Often reduces O(n²) brute-force solutions to O(n).
Usually requires O(1) additional space.
Simple pointer movement can eliminate large parts of the search space.
Complexity

Typical complexity:

Time: O(n)
Space: O(1)

The exact complexity depends on the problem.

For example, 3Sum takes O(n²) because it performs a two-pointer scan
for each possible first element.