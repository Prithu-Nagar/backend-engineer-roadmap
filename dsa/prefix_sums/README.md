# Prefix Sums & Difference Arrays

This directory contains prefix-sum and difference-array implementations covered
in the Backend Engineer Roadmap.

## Day 29 — Prefix Sums / Difference Arrays

Prefix sums preprocess cumulative information so repeated range queries can be
answered efficiently. Difference arrays represent range updates by storing
changes at boundaries and reconstructing the final values with a prefix sum.

Topics:

- Prefix sum construction
- Constant-time range-sum queries after preprocessing
- Prefix/suffix products
- Difference arrays for range updates
- Boundary updates
- Time and space trade-offs

Implementations:

- `product_of_array_except_self.py` — LeetCode: Product of Array Except Self
- `range_sum_query_immutable.py` — LeetCode: Range Sum Query - Immutable

## Prefix Sum Pattern

```text
Input array
    |
    v
Build cumulative state
    |
    v
prefix[i] = information through index i
    |
    v
Answer range queries from precomputed state
```

For a sum array with prefix `P`:

```text
sum(left, right) = P[right + 1] - P[left]
```

## Difference Array Pattern

For a range update `[left, right]`:

```text
diff[left] += value
diff[right + 1] -= value
```

A final prefix pass reconstructs the updated array.

## Complexity

For `n` input values:

- Prefix preprocessing: O(n)
- Range query: O(1)
- Difference-array update: O(1)
- Final reconstruction: O(n)
- Prefix/difference storage: O(n)

The pattern is especially useful when many range queries or range updates must
be processed efficiently.
