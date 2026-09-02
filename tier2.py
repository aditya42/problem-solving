import unittest
from dataclasses import dataclass
from typing import Optional
from collections import deque


def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result: list[list[int]] = []

    for index in range(len(nums) - 2):
        if nums[index] > 0:
            break

        if index > 0 and nums[index] == nums[index - 1]:
            continue

        left = index + 1
        right = len(nums) - 1

        while left < right:
            total = nums[index] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[index], nums[left], nums[right]])
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1

                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


def three_sum_closest(nums: list[int], target: int) -> int:
    if len(nums) < 3:
        raise ValueError("at least three numbers are required")

    nums.sort()
    closest = nums[0] + nums[1] + nums[2]

    for index in range(len(nums) - 2):
        left = index + 1
        right = len(nums) - 1

        while left < right:
            total = nums[index] + nums[left] + nums[right]

            if abs(total - target) < abs(closest - target):
                closest = total

            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                return target
    return closest


def sort_colors(nums: list[int]) -> None:
    low = 0
    current = 0
    high = len(nums) - 1

    while current <= high:
        if nums[current] == 0:
            nums[low], nums[current] = nums[current], nums[low]
            low += 1
            current += 1

        elif nums[current] == 1:
            current += 1

        else:
            nums[current], nums[high] = nums[high], nums[current]
            high -= 1


def product_except_self(nums: list[int]) -> list[int]:
    result = [1] * len(nums)
    prefix = 1

    for index in range(len(nums)):
        result[index] = prefix
        prefix *= nums[index]

    suffix = 1

    for index in range(len(nums) - 1, -1, -1):
        result[index] *= suffix
        suffix *= nums[index]

    return result


def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts = {0: 1}
    prefix_sum = 0
    total = 0

    for number in nums:
        prefix_sum += number
        total += prefix_counts.get(prefix_sum - k, 0)
        prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1

    return total


def max_subarray(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must not be empty")

    current = nums[0]
    best = nums[0]

    for number in nums[1:]:
        current = max(number, current + number)
        best = max(best, current)

    return best


def binary_search(nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if nums[middle] == target:
            left = middle + 1
        else:
            right = middle - -1

    return -1


def search_rotated(nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while right >= left:
        middle = left + (right - left) // 2
        if nums[middle] == target:
            return middle

        if nums[left] <= nums[middle]:
            if nums[left] <= target <= nums[middle]:
                right = middle - 1
            else:
                left = middle + 1

        else:
            if nums[middle] < target <= nums[right]:
                left = middle + 1
            else:
                right = middle - 1

    return -1


def search_range(nums: list[int], target: int) -> list[int]:
    def boundary(find_first: bool) -> int:
        left = 0
        right = len(nums) - 1
        answer = -1

        while left <= right:
            middle = left + (right - left) // 2

            if nums[middle] == target:
                answer = middle

                if find_first:
                    right = middle - 1
                else:
                    left = middle + 1

            elif nums[middle] < target:
                left = middle + 1
            else:
                right = middle - 1

        return answer

    return [boundary(True), boundary(False)]


def daily_temperatures(temperatures: list[int]) -> list[int]:
    result = [0] * len(temperatures)
    stack: list[int] = []

    for index, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            previous_index = stack.pop()
            result[previous_index] = index - previous_index

        stack.append(index)

    return result


def is_valid_parentheses(s: str) -> bool:
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    stack: list[str] = []

    for char in s:
        if char in "([{":
            stack.append(char)

        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            return False

    return not stack


class MinStack:
    def __init__(self):
        self.stack: list[tuple[int, int]] = []

    def push(self, value: int) -> None:
        current_min = value if not self.stack else min(value, self.stack[-1][1])
        self.stack.append((value, current_min))

    def pop(self) -> None:
        if not self.stack:
            raise IndexError("pop from empty MinStack")

        self.stack.pop()

    def top(self) -> int:
        if not self.stack:
            raise IndexError("top from empty MinStack")

        return self.stack[-1][0]

    def get_min(self) -> int:
        if not self.stack:
            raise IndexError("get_min from empty MinStack")

        return self.stack[-1][1]


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    previous = None
    current = head

    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node

    return previous


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []

    result: list[list[int]] = []
    queue = deque([root])

    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

    result.append(level)

    return result


def build_linked_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy

    for value in values:
        tail.next = ListNode(value)
        tail = tail.next

    return dummy.next


def linked_list_to_list(head: Optional[ListNode]) -> list[int]:
    values: list[int] = []

    while head:
        values.append(head.val)
        head = head.next

    return values


class TestTier2(unittest.TestCase):
    def test_three_sum(self):
        self.assertEqual(
            three_sum([-1, 0, 1, 2, -1, -4]),
            [[-1, -1, 2], [-1, 0, 1]],
        )
        self.assertEqual(three_sum([0, 1, 1]), [])
        self.assertEqual(three_sum([0, 0, 0]), [[0, 0, 0]])

    def test_three_sum_closest(self):
        self.assertEqual(three_sum_closest([-1, 2, 1, -4], 1), 2)
        self.assertEqual(three_sum_closest([0, 0, 0], 1), 0)

    def test_sort_colors(self):
        nums = [2, 0, 2, 1, 1, 0]
        sort_colors(nums)
        self.assertEqual(nums, [0, 0, 1, 1, 2, 2])

        nums = [2, 0, 1]
        sort_colors(nums)
        self.assertEqual(nums, [0, 1, 2])

    def test_product_except_self(self):
        self.assertEqual(
            product_except_self([1, 2, 3, 4]),
            [24, 12, 8, 6],
        )
        self.assertEqual(
            product_except_self([-1, 1, 0, -3, 3]),
            [0, 0, 9, 0, 0],
        )

    def test_subarray_sum(self):
        self.assertEqual(subarray_sum([1, 1, 1], 2), 2)
        self.assertEqual(subarray_sum([1, 2, 3], 3), 2)
        self.assertEqual(subarray_sum([1, -1, 0], 0), 3)

    def test_max_subarray(self):
        self.assertEqual(
            max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]),
            6,
        )
        self.assertEqual(max_subarray([1]), 1)
        self.assertEqual(max_subarray([-3, -2, -5]), -2)

    def test_binary_search(self):
        self.assertEqual(binary_search([-1, 0, 3, 5, 9, 12], 9), 4)
        self.assertEqual(binary_search([-1, 0, 3, 5, 9, 12], 2), -1)

    def test_search_rotated(self):
        self.assertEqual(
            search_rotated([4, 5, 6, 7, 0, 1, 2], 0),
            4,
        )
        self.assertEqual(
            search_rotated([4, 5, 6, 7, 0, 1, 2], 3),
            -1,
        )

    def test_search_range(self):
        self.assertEqual(
            search_range([5, 7, 7, 8, 8, 10], 8),
            [3, 4],
        )
        self.assertEqual(
            search_range([5, 7, 7, 8, 8, 10], 6),
            [-1, -1],
        )
        self.assertEqual(search_range([], 0), [-1, -1])

    def test_daily_temperatures(self):
        self.assertEqual(
            daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
            [1, 1, 4, 2, 1, 1, 0, 0],
        )
        self.assertEqual(
            daily_temperatures([30, 40, 50, 60]),
            [1, 1, 1, 0],
        )

    def test_valid_parentheses(self):
        self.assertTrue(is_valid_parentheses("()"))
        self.assertTrue(is_valid_parentheses("()[]{}"))
        self.assertFalse(is_valid_parentheses("(]"))
        self.assertFalse(is_valid_parentheses("([)]"))
        self.assertTrue(is_valid_parentheses("{[]}"))

    def test_min_stack(self):
        stack = MinStack()
        stack.push(-2)
        stack.push(0)
        stack.push(-3)

        self.assertEqual(stack.get_min(), -3)
        stack.pop()
        self.assertEqual(stack.top(), 0)
        self.assertEqual(stack.get_min(), -2)

    def test_linked_list_cycle(self):
        head = ListNode(3)
        second = ListNode(2)
        third = ListNode(0)
        fourth = ListNode(-4)

        head.next = second
        second.next = third
        third.next = fourth
        fourth.next = second

        self.assertTrue(has_cycle(head))

        no_cycle = build_linked_list([1, 2, 3])
        self.assertFalse(has_cycle(no_cycle))

    def test_reverse_linked_list(self):
        head = build_linked_list([1, 2, 3, 4, 5])
        reversed_head = reverse_list(head)

        self.assertEqual(
            linked_list_to_list(reversed_head),
            [5, 4, 3, 2, 1],
        )

        self.assertIsNone(reverse_list(None))

    def test_level_order(self):
        root = TreeNode(
            3,
            left=TreeNode(9),
            right=TreeNode(
                20,
                left=TreeNode(15),
                right=TreeNode(7),
            ),
        )

        self.assertEqual(
            level_order(root),
            [[3], [9, 20], [15, 7]],
        )

        self.assertEqual(level_order(None), [])
