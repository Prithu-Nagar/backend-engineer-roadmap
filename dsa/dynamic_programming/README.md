# Dynamic Programming

This directory contains Dynamic Programming implementations and interview-oriented problems covered throughout the Backend Engineer Roadmap.

The focus is on understanding:

- DP state
- Recurrence relations
- Base cases
- Memoization
- Tabulation
- Space optimization
- Common 1D DP patterns
- Common 2D DP patterns
- Grid/state formulation

---

## Topics

### 1D Dynamic Programming

1D DP problems typically involve a sequence where the current state depends on one or more previous states.

Common examples:

- Climbing Stairs
- House Robber
- Min Cost Climbing Stairs
- Fibonacci

A common state representation is:

```text
dp[i]
```

where `dp[i]` represents the solution to the subproblem ending at position `i`.

---

### 2D Dynamic Programming

2D DP problems typically use a table where the state depends on two dimensions.

A common representation is:

```text
dp[row][col]
```

where each cell represents the solution to a subproblem associated with a particular row and column.

This pattern is commonly used for:

- Grid problems
- Matrix problems
- Sequence comparison
- Problems where two variables define the state

Common examples:

- Unique Paths
- Minimum Path Sum
- Longest Common Subsequence

---

## State Formulation

The most important step in Dynamic Programming is identifying the state.

For a grid problem:

```text
dp[row][col]
```

can represent the best or number of possible solutions for reaching or processing that particular cell.

For sequence comparison:

```text
dp[i][j]
```

can represent the solution considering the first `i` elements of one sequence and the first `j` elements of another sequence.

The state definition determines the recurrence relation.

---

## Recurrence Relations

A recurrence relation describes how the current state can be calculated from previously solved states.

For example, Unique Paths can use:

```text
dp[row][col] = dp[row - 1][col] + dp[row][col - 1]
```

because a cell can be reached from:

- The cell above it
- The cell to its left

For Minimum Path Sum:

```text
dp[row][col] = min(
    dp[row - 1][col],
    dp[row][col - 1]
) + grid[row][col]
```

For Longest Common Subsequence, when the current characters match:

```text
dp[i][j] = dp[i - 1][j - 1] + 1
```

Otherwise:

```text
dp[i][j] = max(
    dp[i - 1][j],
    dp[i][j - 1]
)
```

---

## Memoization

Memoization is a top-down Dynamic Programming approach.

The solution is usually expressed recursively, while already-computed states are stored and reused.

Example:

```text
Problem
   ↓
Subproblem
   ↓
Check cache
 ┌─┴─┐
Hit  Miss
 ↓     ↓
Return  Compute
        ↓
      Store
```

---

## Tabulation

Tabulation is a bottom-up Dynamic Programming approach.

The solution starts from known base cases and builds toward the final answer.

Example:

```text
Base Cases
    ↓
dp[1]
    ↓
dp[2]
    ↓
dp[3]
    ↓
Final Answer
```

For 2D DP, the same idea is extended to a table:

```text
Base States
    ↓
First Row / Column
    ↓
Remaining Cells
    ↓
Final State
```

---

## Memoization vs Tabulation

| Feature | Memoization | Tabulation |
| --- | --- | --- |
| Approach | Top-down | Bottom-up |
| Usually uses | Recursion | Iteration |
| Storage | Dictionary / Array | Array / Table |
| Computes | Required states | States in chosen order |
| Recursion stack | Yes | No |
| Space optimization | Sometimes | Often easier |

---

## Space Optimization

Many DP problems do not require the entire DP table after a state has been processed.

For example, some 1D DP problems only require the previous one or two states.

Instead of:

```text
dp = [0, 1, 1, 2, 3, ...]
```

we can maintain:

```text
previous
current
```

This can reduce space from:

```text
O(n)
```

to:

```text
O(1)
```

Similarly, some 2D DP problems only require the previous row and the current row, allowing the space complexity to be reduced.

---

# Problems

## Climbing Stairs

LeetCode 70

File:

`climbing_stairs.py`

Pattern:

```text
dp[i] = dp[i - 1] + dp[i - 2]
```

The number of ways to reach a step depends on the number of ways to reach the previous two steps.

---

## House Robber

LeetCode 198

File:

`house_robber.py`

Pattern:

```text
dp[i] = max(
    dp[i - 1],
    dp[i - 2] + nums[i]
)
```

At each house, choose between:

- Skipping the current house
- Robbing the current house and using the best valid result from two positions earlier

---

## Min Cost Climbing Stairs

LeetCode 746

File:

`min_cost_climbing_stairs.py`

Pattern:

```text
dp[i] = cost[i] + min(
    dp[i - 1],
    dp[i - 2]
)
```

The solution builds the minimum cost required to reach each step.

---

## Unique Paths

LeetCode 62

File:

`unique_paths.py`

Pattern:

```text
dp[row][col] = dp[row - 1][col] + dp[row][col - 1]
```

A robot can move only right or down.

The number of paths to a cell is the sum of the paths to the cell above and the cell to the left.

The implementation uses space optimization so that the complete 2D table does not need to be stored.

---

## Minimum Path Sum

LeetCode 64

File:

`min_path_sum.py`

Pattern:

```text
dp[row][col] = min(
    dp[row - 1][col],
    dp[row][col - 1]
) + grid[row][col]
```

The objective is to find the minimum possible sum along a path from the top-left cell to the bottom-right cell.

The implementation uses a 1D DP array to reduce space complexity.

---

## Longest Common Subsequence

LeetCode 1143

File:

`longest_common_subsequence.py`

Pattern:

If the current characters match:

```text
dp[i][j] = dp[i - 1][j - 1] + 1
```

Otherwise:

```text
dp[i][j] = max(
    dp[i - 1][j],
    dp[i][j - 1]
)
```

The problem demonstrates how 2D DP can be used when the state depends on positions in two different sequences.

The implementation uses a 1D array to optimize space.

---

# Complexity Pattern

A common 1D DP implementation has:

```text
Time: O(n)
```

Space can be:

```text
O(n)
```

with a DP array, or:

```text
O(1)
```

when only a fixed number of previous states are required.

For common 2D DP problems:

```text
Time: O(m × n)
```

where `m` and `n` represent the dimensions of the state space.

Space can be:

```text
O(m × n)
```

when the complete DP table is stored.

Space can often be reduced to:

```text
O(n)
```

when only the previous row or a fixed number of previous states is required.

---

# Learning Approach

For each Dynamic Programming problem:

1. Understand the problem.
2. Identify the state.
3. Define what each DP state represents.
4. Find the recurrence.
5. Determine the base cases.
6. Decide between memoization and tabulation.
7. Implement the solution.
8. Analyze time and space complexity.
9. Look for possible state compression.
10. Verify the solution with small examples.

---

# Key Patterns

When approaching a new Dynamic Programming problem, ask:

## What is the state?

What information is required to describe a subproblem?

### What are the base cases?

What states can be solved immediately?

### What is the transition?

How does the current state depend on previous states?

### What is the direction?

Should the table be built:

- From left to right?
- From top to bottom?
- From smaller states to larger states?

### Can the state be compressed?

Do we actually need the complete DP table, or only the previous row/state?

These questions form the foundation for recognizing and solving Dynamic Programming problems.

---

## Day 31 — Advanced DP: Knapsack Pattern

Day 31 introduces the 0/1 Knapsack pattern and connects it to subset-sum
problems.

Topics include:

- Choosing an item at most once
- Capacity-based DP state
- Include vs exclude transitions
- Reverse iteration for 0/1 knapsack
- Subset-sum transformation
- Space optimization from 2D to 1D DP

Files:

- `knapsack_01.py`
- `partition_equal_subset_sum.py`
- `coin_change.py`

The key distinction is that 0/1 decisions require reverse iteration when a
1D state array is reused; forward iteration can accidentally reuse the same
item multiple times in one pass.

---

## Day 32 — Subsequence / State DP

Day 32 extends Dynamic Programming into subsequence and state-based problems.

Topics:

- Longest Increasing Subsequence
- State transitions over sequence positions
- `O(n log n)` LIS optimization with a tails array
- Decode Ways state transitions
- Constant-space DP for linear state problems

Implementations:

- `longest_increasing_subsequence.py`
- `decode_ways.py`
