from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    ans, stack = [], []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        ans.append(current.val)
        current = current.right
    return ans


def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    if not root:
        return []
    ans = []
    stack = [root]
    while stack:
        node = stack.pop()
        ans.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return ans


def invert_binary_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root:
        root.left, root.right = (
            inorder_traversal(root.right),
            invert_binary_tree(root.left),
        )
    return root


def path_sum_tree(root: Optional[TreeNode], target_sum: int) -> bool:
    return has_path_sum(root, target_sum)


def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target_sum
    remaining = target_sum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


def symmetric_tree(root: Optional[TreeNode]) -> bool:
    def mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if not a or not b:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return True if not root else mirror(root.left, root.right)


def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    def build(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(nums) - 1)


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = 0

    def depth(node: Optional[TreeNode]) -> int:
        nonlocal diameter
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        diameter = max(diameter, left + right)
        return 1 + max(left, right)

    depth(root)
    return diameter


def count_complete_tree_nodes(root: Optional[TreeNode]) -> int:
    def left_height(node: Optional[TreeNode]) -> int:
        height = 0
        while node:
            height += 1
            node = node.left
        return height

    def right_height(node: Optional[TreeNode]) -> int:
        height = 0
        while node:
            height += 1
            node = node.right
        return height

    if not root:
        return 0
    lh, rh = left_height(root), right_height(root)
    if lh == rh:
        return (1 << lh) - 1
    return (
        1 + count_complete_tree_nodes(root.left) + count_complete_tree_nodes(root.right)
    )


def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    while root:
        if root.val == val:
            return root
        root = root.left if val < root.val else root.right
    return None


def balanced_binary_tree(root: Optional[TreeNode]) -> bool:
    def height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) != -1


def closed_bst_values(root: TreeNode, target: float) -> int:
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        root = root.left if target < root.val else root.right
    return closest


def subtree_of_another_tree(
    root: Optional[TreeNode], sub_root: Optional[TreeNode]
) -> bool:
    def same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if not a or not b:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if not sub_root:
        return True
    if not root:
        return False
    return (
        same(root, sub_root)
        or subtree_of_another_tree(root.left, sub_root)
        or subtree_of_another_tree(root.right, sub_root)
    )
