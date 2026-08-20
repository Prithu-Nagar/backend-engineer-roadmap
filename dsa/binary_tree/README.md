# Binary Trees

This directory contains binary tree problems solved as part of the Backend Engineer Roadmap.

The focus is on recursive tree traversal and identifying common binary-tree problem patterns.

---

## Problems

| Problem | Pattern | Time | Space |
|---|---|---:|---:|
| Maximum Depth of Binary Tree | DFS / Recursion | O(n) | O(h) |
| Invert Binary Tree | DFS / Recursion | O(n) | O(h) |
| Same Tree | DFS / Recursion | O(n) | O(h) |

Where `n` is the number of nodes and `h` is the height of the tree.

---

## Common Pattern

Many binary-tree problems can be solved recursively:

```python
if root is None:
    return base_case

left = solve(root.left)
right = solve(root.right)

return combine(left, right)
```

The key idea is to solve the problem for the left and right subtrees and combine their results.

---

## Problems

### Maximum Depth of Binary Tree

Finds the maximum depth of a binary tree using recursive DFS.

**File:** `maximum_depth.py`

---

### Invert Binary Tree

Swaps the left and right children of every node.

**File:** `invert_binary_tree.py`

---

### Same Tree

Checks whether two binary trees have the same structure and node values.

**File:** `same_tree.py`

---

### Binary Tree Level Order Traversal

Traverses the tree level by level using a queue-based breadth-first search.

**File:** `binary_tree_level_order_traversal.py`

---

## Key Takeaways

- Recursion is a natural approach for binary trees.
- Always consider the base case first.
- Tree traversal usually visits each node once.
- Recursive space complexity depends on tree height.
- A balanced tree has `O(log n)` height.
- A skewed tree can have `O(n)` height.
