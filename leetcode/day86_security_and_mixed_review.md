# Day 86 — Security and Mixed Interview Review

**Goal:** Attempt four medium problems and one hard problem under timed conditions, then review the invariant and edge cases.

## Suggested problem set

1. **Daily Temperatures** — monotonic stack; medium.
2. **Minimum Window Substring** — variable sliding window and character counts; hard attempt.
3. **Network Delay Time** — Dijkstra's algorithm; medium.
4. **Search in Rotated Sorted Array** — binary search with a sorted-half invariant; medium.
5. **Largest Rectangle in Histogram** — monotonic stack and boundary reasoning; hard/advanced review.

Choose four medium problems and one hard attempt from this set. Difficulty labels can vary by platform; prioritize the assigned count and honest timed practice.

## Security reasoning prompts

- Where should authentication end and resource-level authorization begin?
- Why must SQL values be parameterized?
- Which data should never appear in logs or client-facing errors?
- How do CSRF, CORS, and host validation solve different problems?
- Which invariants belong in database constraints rather than application checks?

## Timed workflow

- Clarify constraints and state the brute-force approach.
- Explain the invariant before coding.
- Test empty input, duplicates, boundary indices, and adversarial cases.
- State time and auxiliary-space complexity.
- Record whether each solution was independent, hinted, or reviewed afterward.

## Review template

- Problem:
- Pattern / invariant:
- Complexity:
- Edge cases:
- Outcome and mistake:
- Re-solve date:

## Success criteria

- [ ] Four medium problems attempted.
- [ ] One hard problem attempted, even if not completed.
- [ ] Security answers distinguish authentication, authorization, validation, and integrity.
- [ ] Incorrect or hinted solutions are scheduled for a repeat attempt.
