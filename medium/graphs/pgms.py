from multiprocessing import dummy
from typing import Optional

from easy.graphs.pgms import reverse_linked_list
from medium.BST.pgms import ListNode


def add_two_numbers(
    l1: Optional[ListNode], l2: Optional[LilyPondStyle]
) -> Optional[ListNode]:
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        total = carry
        if l1:
            total += l1.val
            l1 = l1.next
        if l2:
            total += l2.val
            l2 = l2.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next


def partition_list(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    before = before_tail = ListNode()
    after = after_tail = ListNode()
    while head:
        nxt = head.next
        head.next = None
        if head.val < x:
            before_tail.next = head
            before_tail = head
        else:
            after_tail.next = head
            after_tail = head
        head = nxt
    before_tail.next = after.next
    return before.next


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next


def odd_even_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head


def linked_list_cycle_ii(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


def swap_nodes_in_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        first.next = second.next
        second.next = first
        prev.next = second
        prev = first
    return dummy.next


def delete_duplicates_sorted_list_ii(head: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    prev = dummy
    while head:
        if head.next and head.val == head.next.val:
            duplicate = head.val
            while head and head.val == duplicate:
                head = head.next
            prev.next = head
        else:
            prev = head
            head = head.next
    return dummy.next


def rotate_list(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or not head.next or k == 0:
        return head
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
    k %= length
    if k == 0:
        return head
    tail.next = head
    steps = length - k
    new_tail = tail
    while steps:
        new_tail = new_tail.next
        steps -= 1
    new_head = new_tail.next
    new_tail.next = None
    return new_head


class DoublyNode:
    def __init__(
        self,
        val: int,
        prev: Optional["DoublyNode"] = None,
        next: Optional["DoublyNode"] = None,
        child: Optional["DoublyNode"] = None,
    ):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


def flatten_multilevel_doubly_linked_list(
    head: Optional[DoublyNode],
) -> Optional[DoublyNode]:
    if not head:
        return None
    dummy = DoublyNode(0)
    prev = dummy
    stack = [head]
    while stack:
        node = stack.pop()
        prev.next = node
        node.prev = prev
        if node.next:
            stack.append(node.next)
        if node.child:
            stack.append(node.child)
            node.child = None
        prev = node
    result = dummy.next
    result.prev = None
    return result


def reorder_list(head: Optional[ListNode]) -> None:
    if not head or not head.next:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    second = reverse_linked_list(slow.next)
    slow.next = None
    first = head
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2


def split_linked_list_in_parts(
    head: Optional[ListNode], k: int
) -> list[Optional[ListNode]]:
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    base, extra = divmod(length, k)
    ans = []
    current = head
    for i in range(k):
        ans.append(current)
        size = base + (1 if i < extra else 0)
        for _ in range(size - 1):
            if current:
                current = current.next
        if current:
            nxt = current.next
            current.next = None
            current = nxt
    return ans
