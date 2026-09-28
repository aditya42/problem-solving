import re


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


def isPalin(n):
    rev = reverseBits(n)
    return n == rev


def largestPalin(string):
    words = re.findall(r"\b\w+\b", string)
    palindrome_words = filter(isPalindrome, words)
    largest_palindrome = max(palindrome_words, key=len, default=None)
    print(largest_palindrome)


def countPalin(str):
    count = 0
    listOfWords = str.split(" ")
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


def maxLengthNonPalinString(str):
    n = len(str)
    ch = str[0]
    i = 1
    for i in range(1, n):
        if str[i] != ch:
            break
    if i == n:
        return 0
    if isPalindrome(str):
        return n - 1
    return n


if __name__ == "__main__":
    print(isPalindrome("abba"))
    s = "Too hot to hoot."
    print("true" if isPalinSent(s) else "false")
    n = 9
    print("Yes" if isPalin(n) else "No")
    string = "my name is aditya"
    largestPalin(string)
    countPalin("nitin speaks malayalam")
    print("true" if canFormPalindrome("geeksforgeeks") else "false")
    str = "abba"
    print(maxLengthNonPalinString(str))
