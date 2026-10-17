# Greedy Algorithms

This directory contains greedy-algorithm implementations covered throughout
the Backend Engineer Roadmap.

## Day 27 — Greedy Algorithms

Greedy algorithms make the best locally available choice at each step with the
goal of producing an optimal overall solution.

Topics:

- Local-choice strategy
- Greedy-choice property
- Optimal substructure
- Recognizing when greedy is appropriate
- Proving or validating a greedy strategy
- Time and space complexity

Implementations:

- `best_time_to_buy_sell_stock.py` — Best Time to Buy and Sell Stock
- `jump_game.py` — Jump Game
- `gas_station.py` — Gas Station

## Common Greedy Pattern

```text
Input
  |
  v
Evaluate the current state
  |
  v
Make the best local choice
  |
  v
Update the state
  |
  v
Repeat until the problem is solved
```

A greedy solution should not be accepted merely because the local choice looks
reasonable. The choice must be justified by the problem's structure.

---

## Day 38 — Heap + Greedy

Day 38 applies greedy choices with a max-heap to repeatedly select the most
useful remaining option.

Problems:

- Task Scheduler
- Reorganize String

The implementations are stored in `dsa/heap/` because the heap is the primary
supporting data structure for both solutions.

---

## Day 78 — Backtracking and Greedy Interview Review

Day 78 revisits backtracking and greedy reasoning through existing implementations.
No duplicate LeetCode solution files are added.

Review set:

- **Combination Sum II** — backtracking, duplicate avoidance, and pruning
  (`../recursion/combination_sum_ii.py`)
- **Palindrome Partitioning** — recursive partitioning with constraint checks
  (`../recursion/palindrome_partitioning.py`)
- **Jump Game** — farthest-reachable invariant (`jump_game.py`)
- **Gas Station** — greedy feasibility and reset reasoning (`gas_station.py`)

For each problem, explain the state or invariant, identify pruning or greedy
choice justification, trace an edge case, and state time and auxiliary-space
complexity.
