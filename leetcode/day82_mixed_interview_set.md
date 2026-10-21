# Day 82 — Mixed LeetCode Interview Set

Complete five mixed problems under timed conditions. For each problem, state
the pattern, invariant or state transition, edge cases, time complexity, and
auxiliary-space complexity before checking a solution.

## Problems

1. **Coin Change** — Dynamic programming; minimum number of coins for a target.
   - State: `dp[amount]` is the fewest coins needed to form `amount`.
   - Target complexity: `O(amount * number_of_coins)` time, `O(amount)` space.
2. **Word Search** — Backtracking; search adjacent cells without reusing a cell.
   - State: current cell, word index, and visited cells.
   - Prune on bounds, mismatched characters, or revisited cells.
3. **Combination Sum** — Backtracking; reuse positive candidates while reaching a target.
   - State: candidate start index, remaining target, and current path.
   - Undo each choice and avoid duplicate candidate values.
4. **House Robber** — Dynamic programming; maximize non-adjacent selections.
   - State transition: `current = max(previous_best, two_back + value)`.
   - Include empty and single-element inputs.
5. **Longest Increasing Subsequence** — Dynamic programming / binary-search optimization.
   - Compare `O(n^2)` DP with `O(n log n)` tails-based optimization.

## Timed Practice

- [ ] Spend 8–12 minutes per problem before reviewing hints.
- [ ] Write down the brute-force approach and why it is too expensive.
- [ ] Derive the DP state or recursive state before coding.
- [ ] Test empty input, smallest valid input, duplicates, and unreachable targets.
- [ ] Re-solve the weakest two problems without notes.

## Review Notes

| Problem | Pattern identified? | Correctness explanation | Complexity | Revisit |
|---|---|---|---|---|
| Coin Change | | | | |
| Word Search | | | | |
| Combination Sum | | | | |
| House Robber | | | | |
| Longest Increasing Subsequence | | | | |
