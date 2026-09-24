# Recursion & Backtracking

This directory contains recursion and backtracking problems covered throughout the Backend Engineer Roadmap.

The focus is on understanding:

- Recursive problem decomposition
- Base cases
- Recursive cases
- Call stack behavior
- Decision trees
- Backtracking
- State restoration
- Constraint exploration
- Common interview patterns

---

## Recursion

Recursion is a technique where a function solves a problem by calling itself on a smaller version of the same problem.

A recursive solution normally contains:

1. **Base case**
2. **Recursive case**

### Example

```python
def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)
```

The base case stops the recursion.

The recursive case reduces the problem toward the base case.

### Recursion Flow

A recursive call can be visualized as:

```text
Problem
   |
   v
Smaller Problem
   |
   v
Smaller Problem
   |
   v
Base Case
   |
   v
Return
   |
   v
Previous Call
   |
   v
Final Answer
```

---

## Backtracking

Backtracking explores multiple possible choices.

The general pattern is:

```text
Choose
  |
  v
Explore
  |
  v
Undo Choice
  |
  v
Try Next Choice
```

Backtracking is useful when a problem requires exploring combinations, permutations, subsets, paths, or other possible configurations.

### General Backtracking Template

```python
def backtrack(state):
    if is_complete(state):
        result.append(state.copy())
        return

    for choice in choices:
        make_choice(choice)
        backtrack(state)
        undo_choice(choice)
```

The important idea is that the state must be restored after exploring a branch.

---

## Common Patterns

### Subsets

At every element there are usually two choices:

- Include
- Exclude

This creates a binary decision tree.

For `n` elements, there are:

**2^n possible subsets.**

### Permutations

At every level, choose one unused element.

Example:

```text
[1, 2, 3]

Choose 1
 ├── Choose 2
 │    └── Choose 3
 └── Choose 3
      └── Choose 2
```

The number of permutations is:

**n!**

### Combination Sum

Combination problems generally explore candidate choices while tracking the current sum.

Important considerations include:

- Current path
- Remaining target
- Candidate index
- Whether a candidate can be reused
- Pruning invalid branches

---

## Recursion vs Backtracking

| Concept | Recursion | Backtracking |
|---|---|---|
| Main idea | Solve a smaller subproblem | Explore possible choices |
| State | Usually simpler | Explicitly maintained |
| Undo operation | Not always required | Usually required |
| Common use | Trees, divide-and-conquer | Subsets, permutations, combinations |
| Search space | May be linear or tree-shaped | Often exponential |

---

## Complexity

Many backtracking problems have exponential or factorial time complexity.

Examples:

| Problem type | Typical time complexity |
|---|---:|
| Subsets | `O(2^n)` |
| Permutations | `O(n!)` |
| Combination problems | Often exponential |

Space complexity depends on:

- Recursion depth
- Current path
- Result storage

---

## Interview Checklist

When solving a recursion/backtracking problem, ask:

- What is the base case?
- What is the recursive state?
- What choices exist at each step?
- What happens after making a choice?
- When should a branch be pruned?
- What state must be restored?
- What is the recursion depth?
- What is the time complexity?
- What is the auxiliary space complexity?

---

## Problems

### Subsets

**File:** `subsets.py`

**Pattern:**

- Recursion
- Include/exclude
- Backtracking

### Permutations

**File:** `permutations.py`

**Pattern:**

- Backtracking
- Used-element tracking
- Decision tree

### Combination Sum

**File:** `combination_sum.py`

**Pattern:**

- Backtracking
- Remaining target
- Candidate reuse
- Pruning

---

## Day 47 — Backtracking Review

Day 47 revisits backtracking with constraint tracking, duplicate avoidance,
and state restoration.

### N-Queens

**File:** `n_queens.py`

The solution places one queen per row and tracks:

- Occupied columns
- `row - column` diagonals
- `row + column` anti-diagonals
- Board state restoration after each recursive branch

### Combination Sum II

**File:** `combination_sum_ii.py`

The solution sorts candidates so it can:

- Prune when the current value exceeds the remaining target
- Skip duplicate values at the same recursion depth
- Advance the next index so each array element is used at most once

### Palindrome Partitioning

**File:** `palindrome_partitioning.py`

The solution explores every possible next substring and continues only when
that substring is a palindrome.

### Backtracking Review Checklist

- Define the recursive state before writing the loop.
- Identify exactly which choices are legal at each level.
- Prune branches as soon as a constraint is violated.
- Copy result state before later recursive calls mutate it.
- Undo every mutable state change before returning from a branch.
- Handle duplicate choices deliberately rather than deduplicating blindly at the end.

---

## Day 55 — Backtracking Problems

Day 55 applies the backtracking pattern to problems where a solution is
constructed incrementally and invalid branches can be pruned early.

Problems added:

- Restore IP Addresses
- Generate Parentheses
- Combination Sum III

These problems reinforce:

- Choice exploration
- Constraint validation
- Branch pruning
- State restoration
- Building results from a recursion path
