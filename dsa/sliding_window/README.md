# Sliding Window

Sliding Window is a technique for processing contiguous subarrays or substrings efficiently by maintaining a moving range with two pointers.

---

## Core Patterns

### Fixed Window

Use when the window size is fixed at `k`.

```text
[ a b c ] d e
    ↓
 a [ b c d ] e
```

### Variable Window

Use when the window expands and shrinks according to a condition.

```text
left  → shrink
right → expand
```

---

## Typical Complexity

| Metric | Typical complexity |
|---|---|
| Time | `O(n)` when both pointers move only forward |
| Space | `O(1)` for simple numeric windows, or `O(k)` when using a Set/HashMap |

---

## Day 52 — Hashing + Sliding Window

Day 52 expands variable-window patterns with frequency maps and explicit
window invariants.

Added:

- `minimum_window_substring.py` — maintain required character counts
- `longest_repeating_character_replacement.py` — track the dominant frequency
  while allowing at most `k` replacements

The common workflow is:

1. Expand the right pointer.
2. Update frequency state.
3. Check whether the window violates the constraint.
4. Shrink from the left until the invariant is restored.
5. Update the best answer.
