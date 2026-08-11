# Dynamic Programming

This directory contains Dynamic Programming implementations and interview-oriented problems covered throughout the Backend Engineer Roadmap.

The focus is on understanding:

* DP state
* Recurrence relations
* Base cases
* Memoization
* Tabulation
* Space optimization
* Common 1D DP patterns

---

## Topics

### 1D Dynamic Programming

1D DP problems typically involve a sequence where the current state depends on one or more previous states.

Common examples:

* Climbing Stairs
* House Robber
* Min Cost Climbing Stairs
* Fibonacci

A common state representation is:

```text
dp[i]
```

where `dp[i]` represents the solution to the subproblem ending at position `i`.

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
dp[2]
    ↓
dp[3]
    ↓
dp[4]
    ↓
Final Answer
```

---

## Memoization vs Tabulation

| Feature            | Memoization        | Tabulation             |
| ------------------ | ------------------ | ---------------------- |
| Approach           | Top-down           | Bottom-up              |
| Usually uses       | Recursion          | Iteration              |
| Storage            | Dictionary / Array | Array / Table          |
| Computes           | Required states    | States in chosen order |
| Recursion stack    | Yes                | No                     |
| Space optimization | Sometimes          | Often easier           |

---

## Space Optimization

Many 1D DP problems only require the previous one or two states.

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

---

## Problems

### Climbing Stairs

LeetCode 70

File:

`climbing_stairs.py`

Pattern:

```text
dp[i] = dp[i - 1] + dp[i - 2]
```

---

### House Robber

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

---

### Min Cost Climbing Stairs

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

---

## Complexity Pattern

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

---

## Learning Approach

For each Dynamic Programming problem:

1. Understand the problem.
2. Identify the state.
3. Find the recurrence.
4. Determine the base cases.
5. Decide between memoization and tabulation.
6. Implement the solution.
7. Analyze time and space complexity.
8. Look for possible state compression.
