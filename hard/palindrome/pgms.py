from easy.palindrome.pgms import isPalindrome


def findminInsertions(s):
    n = len(s)
    dp = [0] * n
    for l in range(n - 2, -1, -1):
        prev = 0
        for h in range(l + 1, n):
            temp = dp[h]
            if s[l] == s[h]:
                dp[h] = prev
            else:
                dp[h] = min(dp[h], dp[h - 1]) + 1
            prev = temp
    return dp[n - 1]


def palindromePair(arr):
    strMap = {}
    for i in range(len(arr)):
        word = arr[i][::-1]
        strMap[word] = i

    for i in range(len(arr)):
        left = ""
        for j in range(len(arr[i])):
            left += arr[i][j]
            right = arr[i][j + 1 :]
            if left and isPalindrome(left) and right in strMap and strMap[right] != i:
                return True

            if isPalindrome(right) and left in strMap and strMap[right] != i:
                return True

            if isPalindrome(right) and left in strMap and strMap[left] != i:
                return True
    return False


if __name__ == "__main__":
    s = "geeks"
    print(findminInsertions(s))
    arr = ["geekf", "geeks", "or", "keeg", "abc", "bc"]
    if palindromePair(arr):
        print("True")
    else:
        print("False")
