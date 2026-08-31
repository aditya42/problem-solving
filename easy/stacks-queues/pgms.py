from typing import Tuple, Optional


class MyQueue:
    def __init__(self):
        self.input = []
        self.output = []

    def push(self, x: int) -> None:
        self.input.append(x)

    def _shift(self) -> None:
        if not self.output:
            while self.input:
                self.output.append(self.input.pop())

    def pop(self) -> int:
        self._shift()
        return self.output.pop()

    def peek(self) -> int:
        self._shift()
        return self.output[-1]

    def empty(self) -> bool:
        return not self.input and not self.output


def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    stack = []
    nxt = {}
    for value in nums2:
        while stack and value > stack[-1]:
            nxt[stack.pop()] = value
        stack.append(value)
    return [nxt.get(value, -1) for value in nums1]


def backspace_string_compare(s: str, t: str) -> bool:
    def next_valid(text: str, i: int) -> Tuple[Optional[str], int]:
        skip = 0
        while i >= 0:
            if text[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                return text[i], i - 1
            i -= 1
        return None, -1

    i, j = len(s) - 1, len(t) - 1
    while i >= 0 or j >= 0:
        a, i = next_valid(s, i)
        b, j = next_valid(t, j)
        if a != b:
            return False
    return True
