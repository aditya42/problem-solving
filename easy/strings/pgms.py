from collections import Counter


def valid_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def str_str(haystack: str, needle: str) -> int:
    if needle == "":
        return 0
    m = len(needle)
    for i in range(len(haystack) - m + 1):
        if haystack[i : i + m] == needle:
            return i
    return -1


def first_unique_character(s: str) -> int:
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def valid_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


def reverse_string(chars: list[str]) -> None:
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
