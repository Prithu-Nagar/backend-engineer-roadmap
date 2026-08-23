# Binary Search Tree

Binary Search Tree implementations and interview-focused problems.

## Problems

| Problem                            | Pattern           | Complexity |
| ---------------------------------- | ----------------- | ---------- |
| Search in a Binary Search Tree     | BST Search        | O(h)       |
| Validate Binary Search Tree        | Range Validation  | O(n)       |
| Minimum Distance Between BST Nodes | Inorder Traversal | O(n)       |

## Key Concept

For a Binary Search Tree:

left subtree < node < right subtree

Inorder traversal of a valid BST produces values in sorted order.

## Files

- `search_in_bst.py`
- `validate_bst.py`
- `min_diff_in_bst.py`

---

## Day 23 — BST Successor / Predecessor Patterns

Day 23 extends BST problem solving by using the ordering property to reason
about ancestors, successors, predecessors, and inorder position.

| Problem                                    | Pattern                    | Complexity |
| ------------------------------------------ | -------------------------- | ---------- |
| Lowest Common Ancestor of a BST            | Ordered Traversal          | O(h)       |
| Kth Smallest Element in a BST              | Inorder Traversal          | O(h + k)   |

### Lowest Common Ancestor of a BST

For a BST, if both target values are smaller than the current node, the LCA
must be in the left subtree. If both are larger, it must be in the right
subtree. Otherwise, the current node is the split point and therefore the
lowest common ancestor.

**File:** `lowest_common_ancestor_bst.py`

### Kth Smallest Element in a BST

An inorder traversal of a valid BST visits values in ascending order. The kth
visited node is therefore the kth smallest value.

**File:** `kth_smallest_element.py`

### Key Takeaways

- BST ordering can eliminate half of the search space at each level.
- The inorder traversal of a BST is sorted.
- LCA can be found without exploring unrelated subtrees.
- Iterative inorder traversal can avoid storing the full sorted list.
