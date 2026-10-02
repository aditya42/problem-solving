import re

import builtins


def isPalindrome(s):
    return s == s[::-1]


def isPalinSent(s):
    i, j = 0, len(s) - 1

    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() == s[j].lower():
            i += 1
            j -= 1
        else:
            return False
    return True


def reverseBits(n):
    rev = 0

    while n > 0:
        rev = rev << 1
        if n & 1 == 1:
            rev = rev ^ 1
        n = n >> 1
        return rev


def isPalinRev(n):
    rev = reverseBits(n)
    return n == rev


def largestPalin(string):
    words = re.findall(r"\b\w+\b", string)
    palindrome_words = filter(isPalindrome, words)
    largest_palindrome = max(palindrome_words, key=len, default=None)
    print(largest_palindrome)


def countPalin(string):
    count = 0
    listOfWords = string.split(" ")
    for word in listOfWords:
        if isPalindrome(word):
            count += 1
    print(count)


def canFormPalindrome(s):
    mask = 0
    for ch in s:
        bit = ord(ch) - ord("a")
        mask ^= 1 << bit
    return mask == 0 or (mask & (mask - 1)) == 0


def maxLengthNonPalinString(string):
    n = len(string)
    ch = string[0]
    i = 1
    for i in range(1, n):
        if string[i] != ch:
            break
    if i == n:
        return 0
    if isPalindrome(string):
        return n - 1
    return n


MAX_CHAR = 256


def countFreq(str1, freq, len1):
    for i in range(len1):
        freq[ord(str1[i]) - ord("a")] += 1


def canMakePalindrome(freq, len1):
    count_odd = 0
    for i in range(MAX_CHAR):
        if freq[i] % 2 != 0:
            count_odd += 1

    if len1 % 2 == 0:
        if count_odd > 0:
            return False
        else:
            return True

    if count_odd != 1:
        return False

    return True


def findOddAndRemoveItsFreq(freq):
    odd_str = ""
    for i in range(MAX_CHAR):
        if freq[i] % 2 != 0:
            freq[i] -= 1
            odd_str += chr(i + ord("a"))
            return odd_str
    return odd_str


def findPalindromicString(str1):
    len1 = len(str1)

    freq = [0] * MAX_CHAR
    countFreq(str1, freq, len1)

    if not canMakePalindrome(freq, len1):
        return "No Palindromic String"

    odd_str = findOddAndRemoveItsFreq(freq)

    front_str = ""
    rear_str = " "
    for i in range(MAX_CHAR):
        temp = ""
        if freq[i] != 0:
            ch = chr(i + ord("a"))
            for j in range(1, int(freq[i] / 2) + 1):
                temp += ch

            front_str += temp

            rear_str = temp + rear_str

    return front_str + odd_str + rear_str


def minInsertion(str1):
    n = len(str1)
    res = 0
    count = [0 for i in range(26)]
    for i in range(n):
        count[ord(str1[i]) - ord("a")] += 1
    for i in range(26):
        if count[i] % 2 == 1:
            res += 1
    if res == 0:
        return 0
    else:
        return res - 1


MAX_DIGITS = 20


def main():
    K = 5
    total_sum = 0
    count = 0
    i = 1

    while count < K:
        s = builtins.str(i)

        if len(s) % 2 == 0 and isPalindrome(s):
            total_sum += i
            count += 1

        i += 1
    print(f"Sum of first {K} even-length palindrome numbers: {total_sum}")


def printPalindromes(m, n):
    ans = []

    for num in range(m, n + 1):
        rev = 0
        original = num

        while original > 0:
            rev = rev * 10 + original % 10
            original //= 10

        if rev == num:
            ans.append(num)
    return ans


def isPalin(string: str, low: int, high: int):
    while low < high:
        if string[low] != string[high]:
            return False
        high -= 1
        low += 1
    return True


def possiblepalinByRemovingOneChar(string: str) -> int:
    low = 0
    high = len(string) - 1

    while low < high:
        if string[low] == string[high]:
            low += 1
            high -= 1
        else:
            if isPalin(string, low + 1, high):
                return low
            if isPalin(string, low, high - 1):
                return high
            return -1
    return -2


def isPossiblePalindrome(string):
    n = len(string)
    for i in range(n // 2):
        if (
            string[i] != "."
            and string[n - i - 1] != "."
            and string[i] != string[n - i - 1]
        ):
            return False
    return True


def smallestPalindrome(string):
    if not isPossiblePalindrome(string):
        return "Not possible"
    n = len(string)
    string = list(string)

    for i in range(n):
        if string[i] == ".":
            if string[n - i - 1] != ".":
                string[i] = string[n - i - 1]
            else:
                string[i] = string[n - i - 1] = "a"
    return string


if __name__ == "__main__":
    print(isPalindrome("abba"))
    s = "Too hot to hoot."
    print("true" if isPalinSent(s) else "false")
    n = 9
    print("Yes" if isPalinRev(n) else "No")
    string = "my name is aditya"
    largestPalin(string)
    countPalin("nitin speaks malayalam")
    print("true" if canFormPalindrome("geeksforgeeks") else "false")
    str = "abba"
    print(maxLengthNonPalinString(str))
    string1 = "malayalam"
    print(findPalindromicString(string1))
    str1 = "geeksforgeeks"
    print(minInsertion(str1))
    main()
    m = 10
    n = 115
    print(*printPalindromes(m, n))
    string = "abecbea"
    idx = possiblepalinByRemovingOneChar(string)
    if idx == -1:
        print("Not possible")
    elif idx == -2:
        print("possible without removing any character")
    else:
        print("possible by removing char at index", idx)
    string = "ab..e.c.a"
    print("".join(smallestPalindrome(string)))
