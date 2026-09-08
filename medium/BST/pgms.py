import math
from collections import deque, defaultdict
from typing import Optional
from easy.BST.pgms import TreeNode


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def build_tree_preorder_inorder(
    preorder: list[int], inorder: list[int]
) -> Optional[TreeNode]:
    index = {value: i for i, value in enumerate(inorder)}
    pre = 0

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre
        if left > right:
            return None
        value = preorder[pre]
        pre += 1
        root = TreeNode(value)
        mid = index[value]
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(inorder) - 1)


def build_tree_inorder_postorder(
    inorder: list[int], postorder: list[int]
) -> Optional[TreeNode]:
    index = {value: i for i, value in enumerate(inorder)}
    post = len(postorder) - 1

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal post
        if left > right:
            return None
        value = postorder[post]
        post -= 1
        root = TreeNode(value)
        mid = index[value]
        root.right = build(mid + 1, right)
        root.left = build(left, mid - 1)
        return root

    return build(0, len(inorder) - 1)


def build_tree_preorder_postorder(
    preorder: list[int], postorder: list[int]
) -> Optional[TreeNode]:
    post_index = {value: i for i, value in enumerate(postorder)}
    pre = 0

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre
        if left > right or pre >= len(preorder):
            return None
        root = TreeNode(preorder[pre])
        pre += 1
        if left == right or pre >= len(preorder):
            return root
        mid = post_index[preorder[pre]]
        if mid <= right:
            root.left = build(left, mid)
            root.right = build(mid + 1, right - 1)
        return root

    return build(0, len(preorder) - 1)


def binary_tree_level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    ans = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        ans.append(level)
    return ans


def zigzig_level_order(root: Optional[TreeNode]) -> list[list[int]]:
    levels = binary_tree_level_order(root)
    for i in range(1, len(levels), 2):
        levels[i].reverse()
    return levels


def path_sum_ii(root: Optional[TreeNode], target_sum: int) -> list[list[int]]:
    ans = []

    def dfs(node: Optional[TreeNode], remaining: int, path: list[int]) -> None:
        if not node:
            return
        path.append(node.val)
        remaining -= node.val
        if not node.left and not node.right and remaining == 0:
            ans.append(path[:])
        else:
            dfs(node.left, remaining, path)
            dfs(node.right, remaining, path)
        path.pop()

    dfs(root, target_sum, [])
    return ans


def flip_equiv(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    if not root1 or not root2:
        return root1 is root2
    if root1.val != root2.val:
        return False
    return (
        flip_equiv(root1.left, root2.left) and flip_equiv(root1.right, root2.right)
    ) or (flip_equiv(root1.left, root2.right) and flip_equiv(root1.left, root2.left))


def sum_root_to_leaf_numbers(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode], value: int) -> int:
        if not node:
            return 0
        value = value * 10 + node.val
        if not node.left and not node.right:
            return value
        return dfs(node.left, value) + dfs(node.right, value)

    return dfs(root, 0)


def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    current = head

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal current
        if left > right:
            return None
        mid = (left + right) // 2
        left_tree = build(left, mid - 1)
        root = TreeNode(current.val)
        current = current.next
        root.left = left_tree
        root.right = build(mid + 1, right)
        return root

    return build(0, length - 1)


def path_sum_iii(root: Optional[TreeNode], target_sum: int) -> int:
    prefix = defaultdict(int)
    prefix[0] = 1

    def dfs(node: Optional[TreeNode], running: int) -> int:
        if not node:
            return 0
        running += node.val
        count = prefix[running - target_sum]
        prefix[running] += 1
        count += dfs(node.left, running)
        count += dfs(node.right, running)
        prefix[running] -= 1
        return count

    return dfs(root, 0)


def lowest_common_ancestor_binary_tree(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor_binary_tree(root.left, p, q)
    right = lowest_common_ancestor_binary_tree(root.right, p, q)
    if left and right:
        return root
    return left or right


def level_order_bottom(root: Optional[TreeNode]) -> list[list[int]]:
    return binary_tree_level_order(root)[::-1]


def validate_bst(root: Optional[TreeNode]) -> bool:
    def valid(node: Optional[TreeNode], low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, -math.inf, math.inf)


def binary_tree_longest_consecutive(root: Optional[TreeNode]) -> int:
    best = 0

    def dfs(node: Optional[TreeNode], parent_value: int, length: int) -> None:
        nonlocal best
        if not node:
            return
        length = length + 1 if node.val == parent_value + 1 else 1
        best = max(best, length)
        dfs(node.left, node.val, length)
        dfs(node.right, node.val, length)

    if root:
        dfs(root, root.val - 1, 0)
    return best
