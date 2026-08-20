Add this entire file:

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


1. Base Case
2. Recursive Case


Example:


```python
def factorial(n):
    if n == 0:
        return 1


    return n * factorial(n - 1)

The base case stops the recursion.

The recursive case reduces the problem toward the base case.

Recursion Flow

A recursive call can be visualized as:

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
Backtracking

Backtracking explores multiple possible choices.

The general pattern is:

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

Backtracking is useful when a problem requires exploring combinations, permutations, subsets, paths, or other possible configurations.

General Backtracking Template
def backtrack(state):
    if is_complete(state):
        result.append(state.copy())
        return


    for choice in choices:
        make_choice(choice)


        backtrack(state)


        undo_choice(choice)

The important idea is that the state must be restored after exploring a branch.

Common Patterns
Subsets

At every element there are usually two choices:

Include
Exclude

This creates a binary decision tree.

For n elements, there are:

2^n

possible subsets.

Permutations

At every level, choose one unused element.

Example:

[1, 2, 3]


Choose 1
 ├── Choose 2
 │    └── Choose 3
 └── Choose 3
      └── Choose 2

The number of permutations is:

n!
Combination Sum

Combination problems generally explore candidate choices while tracking the current sum.

Important considerations include:

Current path
Remaining target
Candidate index
Whether a candidate can be reused
Pruning invalid branches
Recursion vs Backtracking
Concept	Recursion	Backtracking
Main idea	Solve smaller subproblem	Explore possible choices
State	Usually simpler	Explicitly maintained
Undo operation	Not always required	Usually required
Common use	Trees, divide-and-conquer	Subsets, permutations, combinations
Search space	May be linear/tree-shaped	Often exponential
Complexity

Many backtracking problems have exponential or factorial time complexity.

Examples:

Subsets → O(2^n)
Permutations → O(n!)
Combination problems → often exponential

Space complexity depends on:

Recursion depth
Current path
Result storage
Interview Checklist

When solving a recursion/backtracking problem, ask:

What is the base case?
What is the recursive state?
What choices exist at each step?
What happens after making a choice?
When should a branch be pruned?
What state must be restored?
What is the recursion depth?
What is the time complexity?
What is the auxiliary space complexity?
Problems
Subsets

File:

subsets.py

Pattern:

Recursion
Include/exclude
Backtracking
Permutations

File:

permutations.py

Pattern:

Backtracking
Used-element tracking
Decision tree
Combination Sum

File:

combination_sum.py

Pattern:

Backtracking
Remaining target
Candidate reuse
Pruning