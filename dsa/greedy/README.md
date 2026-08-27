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
