from __future__ import annotations

from collections import Counter, defaultdict, OrderedDict, deque
from dataclasses import dataclass
import heapq
import unittest
from multiprocessing import dummy
from typing import Optional, cast


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}

    for index, number in enumerate(nums):
        complement = target - number

        if complement in seen:
            return [seen[complement], index]

        seen[number] = index

    return []


def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    counts: dict[str, int] = {}

    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for char in t:
        if char not in counts:
            return False

        counts[char] -= 1

        if counts[char] < 0:
            return False

    return True


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[tuple[str, int], ...], list[str]] = defaultdict(list)

    for word in words:
        signature = tuple(sorted(Counter(word).items()))
        groups[signature].append(word)

    return list(groups.values())


def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        best = max(best, right - left + 1)

    return best


def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    need = Counter(p)
    window = Counter()
    result: list[int] = []
    left = 0

    for right, char in enumerate(s):
        window[char] += 1

        if right - left + 1 > len(p):
            left_char = s[left]
            window[left_char] -= 1

            if window[left_char] == 0:
                del window[left_char]

            left += 1

        if right - left + 1 == len(p) and window == need:
            result.append(left)

    return result


def character_replacement(s: str, k: int) -> int:
    counts: dict[str, int] = {}
    left = 0
    max_frequency = 0
    best = 0

    for right, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        max_frequency = max(max_frequency, counts[char])

        while (right - left + 1) - max_frequency > k:
            counts[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


def compress(chars: list[str]) -> int:
    write = 0
    read = 0

    while read < len(chars):
        current = chars[read]
        group_start = read

        while read < len(chars) and chars[read] == current:
            read += 1

        count = read - group_start
        chars[write] = current
        write += 1

        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1

    return write


def decode_string(s: str) -> str:
    count_stack: list[int] = []
    string_stack: list[str] = []
    current = ""
    number = 0

    for char in s:
        if char.isdigit():
            number = number * 10 + int(char)

        elif char == "[":
            count_stack.append(number)
            string_stack.append(current)
            number = 0
            current = ""

        elif char == "]":
            repeat = count_stack.pop()
            prefix = string_stack.pop()
            current = prefix + current * repeat

        else:
            current += char

    return current


def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    counts = Counter(words)

    ordered = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return [word for word, _ in ordered[:k]]


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda interval: interval[0])
    merged = [intervals[0][:]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


def insert_interval(
    intervals: list[list[int]],
    new_interval: list[int],
) -> list[list[int]]:
    result: list[list[int]] = []
    index = 0
    start, end = new_interval

    while index < len(intervals) and intervals[index][1] < start:
        result.append(intervals[index][:])
        index += 1

    while index < len(intervals) and intervals[index][0] <= end:
        start = min(start, intervals[index][0])
        end = max(end, intervals[index][1])
        index += 1

    result.append([start, end])

    while index < len(intervals):
        result.append(intervals[index][:])
        index += 1

    return result


def find_kth_largest(nums: list[int], k: int) -> int:
    heap: list[int] = []

    for number in nums:
        heapq.heappush(heap, number)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    islands = 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "1":
                continue

            islands += 1
            grid[row][col] = "0"
            queue = deque([(row, col)])

            while queue:
                current_row, current_col = queue.popleft()

                for row_delta, col_delta in (
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ):
                    next_row = current_row + row_delta
                    next_col = current_col + col_delta

                    if (
                        0 <= next_row < rows
                        and 0 <= next_col < cols
                        and grid[next_row][next_col] == "1"
                    ):
                        grid[next_row][next_col] = "0"
                        queue.append((next_row, next_col))

    return islands


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def merge_two_lists(
    list1: Optional[ListNode],
    list2: Optional[ListNode],
) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    tail.next = list1 if list1 else list2

    return dummy.next


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


class TestTier1(unittest.TestCase):
    def test_two_sum(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])
        self.assertEqual(two_sum([3, 3], 6), [0, 1])
        self.assertEqual(two_sum([1, 2, 3], 10), [])

    def test_valid_anagram(self):
        self.assertTrue(is_anagram("anagram", "nagaram"))
        self.assertFalse(is_anagram("rat", "car"))
        self.assertTrue(is_anagram("", ""))

    def test_group_anagrams(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        normalized = {tuple(sorted(group)) for group in result}

        self.assertEqual(
            normalized,
            {
                ("ate", "eat", "tea"),
                ("nat", "tan"),
                ("bat",),
            },
        )

    def test_longest_substring(self):
        self.assertEqual(length_of_longest_substring("abcabcbb"), 3)
        self.assertEqual(length_of_longest_substring("bbbbb"), 1)
        self.assertEqual(length_of_longest_substring("pwwkew"), 3)
        self.assertEqual(length_of_longest_substring(""), 0)

    def test_find_anagrams(self):
        self.assertEqual(find_anagrams("cbaebabacd", "abc"), [0, 6])
        self.assertEqual(find_anagrams("abab", "ab"), [0, 1, 2])
        self.assertEqual(find_anagrams("a", "aa"), [])

    def test_character_replacement(self):
        self.assertEqual(character_replacement("ABAB", 2), 4)
        self.assertEqual(character_replacement("AABABBA", 1), 4)
        self.assertEqual(character_replacement("", 2), 0)

    def test_compress(self):
        chars = ["a", "a", "b", "b", "c", "c", "c"]
        length = compress(chars)
        self.assertEqual(chars[:length], ["a", "2", "b", "2", "c", "3"])

        chars = ["a"] * 12
        length = compress(chars)
        self.assertEqual(chars[:length], ["a", "1", "2"])

    def test_decode_string(self):
        self.assertEqual(decode_string("3[a]2[bc]"), "aaabcbc")
        self.assertEqual(decode_string("3[a2[c]]"), "accaccacc")
        self.assertEqual(decode_string("2[abc]3[cd]ef"), "abcabccdcdcdef")

    def test_top_k_frequent_words(self):
        self.assertEqual(
            top_k_frequent_words(["i", "love", "leetcode", "i", "love", "coding"], 2),
            ["i", "love"],
        )

    def test_merge_intervals(self):
        self.assertEqual(
            merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]),
            [[1, 6], [8, 10], [15, 18]],
        )
        self.assertEqual(merge_intervals([[1, 4], [4, 5]]), [[1, 5]])

    def test_insert_interval(self):
        self.assertEqual(
            insert_interval([[1, 3], [6, 9]], [2, 5]),
            [[1, 5], [6, 9]],
        )
        self.assertEqual(
            insert_interval(
                [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
                [4, 8],
            ),
            [[1, 2], [3, 10], [12, 16]],
        )

    def test_kth_largest(self):
        self.assertEqual(find_kth_largest([3, 2, 1, 5, 6, 4], 2), 5)
        self.assertEqual(
            find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),
            4,
        )

    def test_lru_cache(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.put(3, 3)
        self.assertEqual(cache.get(2), -1)
        cache.put(4, 4)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)

    def test_number_of_islands(self):
        grid = [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
        ]
        self.assertEqual(num_islands(grid), 1)

        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
        self.assertEqual(num_islands(grid), 3)

    def test_merge_two_sorted_lists(self):
        list1 = build_linked_list([1, 2, 4])
        list2 = build_linked_list([1, 3, 4])

        merged = merge_two_lists(list1, list2)

        self.assertEqual(
            linked_list_to_list(merged),
            [1, 1, 2, 3, 4, 4],
        )
