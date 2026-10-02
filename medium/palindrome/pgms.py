def minRemoval(strr):
    hash = [0] * 26

    for char in strr:
        hash[ord(char) - ord("a")] = hash[ord(char) - ord("a")] + 1

    count = 0
    for i in range(26):
        if hash[i] % 2:
            count = count + 1

    return 0 if count == 0 else count - 1


MAX = 256


def printPalindromePos(Str):
    global MAX

    pos = [[] for i in range(MAX)]
    n = len(Str)
    for i in range(n):
        pos[ord(Str[i])].append(i + 1)

    oddCount = 0

    for i in range(MAX):
        if len(pos[i]) % 2 != 0:
            oddCount += 1
            oddChar = i

    if oddCount > 1:
        print("NO PALINDROME")

    for i in range(MAX):
        mid = len(pos[i]) // 2
        for j in range(mid):
            print(pos[i][j], end=" ")

    if oddCount > 0:
        last = len(pos[oddChar]) - 1
        print(pos[oddChar][last], end=" ")
        pos[oddChar].pop()

    for i in range(MAX - 1, -1, -1):
        count = len(pos[i])
        for j in range(count // 2, count):
            print(pos[i][j], end=" ")


def isRotatedPalindrome(s):
    n = len(s)

    concat = s + s

    t = "@"
    for c in concat:
        t += "#" + c
    t += "#$"

    m = len(t)
    P = [0] * m
    center = 0
    right = 0

    for i in range(1, m - 1):
        mirror = 2 * center - i

        if i < right:
            P[i] = min(right - i, P[mirror])

        while t[i + (1 + P[i])] == t[i - (1 + P[i])]:
            P[i] += 1

        if i + P[i] > right:
            center = i
            right = i + P[i]

        if P[i] >= n:
            start = (i - P[i]) // 2
            if start + n <= 2 * n:
                return True
    return False


def maxPalindrome(s, k):
    n = len(s)
    replacements = 0

    for i in range(n // 2):
        j = n - 1 - i
        if s[i] != s[j]:
            replacements += 1
            if replacements > k:
                return "Not Possible"

    s = list(s)
    for i in range((n + 1) // 2):
        j = n - 1 - i
        if i == j:
            s[i] = "9"
        elif s[i] != s[j]:
            if (k - replacements >= 1) and (max(s[i], s[j]) != "9"):
                s[i] = s[j] = "9"
                replacements -= 1
                k -= 2
            else:
                s[i] = s[j] = max(s[i], s[j])
                replacements -= 1
                k -= 1
        elif k - replacements >= 2 and s[i] != "9":
            s[i] = s[j] = "9"
            k -= 2
    return "".join(s)


def reverse(num, i, j):
    while i < j:
        num[i], num[j] = num[j], num[i]
        i += 1
        j -= 1


def nextPlain(n):
    length = len(n)
    num = list(n)

    if length <= 3:
        return "-1"

    mid = length // 2 - 1
    i = mid - 1

    while i >= 0:
        if num[i] < num[i + 1]:
            break
        i -= 1

    if i < 0:
        return "-1"

    smallest = i + 1
    for j in range(i + 2, mid + 1):
        if num[j] > num[i] and num[j] <= num[smallest]:
            smallest = j

    num[i], num[smallest] = num[smallest], num[i]

    num[length - i - 1], num[length - smallest - 1] = (
        num[length - smallest - 1],
        num[length - i - 1],
    )

    reverse(num, i + 1, mid)

    if length % 2 == 0:
        reverse(num, mid + 1, length - i - 2)
    else:
        reverse(num, mid + 2, length - i - 2)

    return "".join(num)


def fact(n):
    ans = 1
    for i in range(1, n + 1):
        ans = ans * i
    return ans


def numberOfPossiblePalindrome(string, n):
    mp = dict()
    for i in range(n):
        if string[i] in mp.keys():
            mp[string[i]] += 1
        else:
            mp[string[i]] = 1

    k = 0
    num = 0
    den = 1
    fi = 0
    for it in mp:
        if mp[it] % 2 == 0:
            fi = mp[it] // 2
        else:
            fi = (mp[it] - 1) // 2
            k += 1

        num = num + fi

        den = den * fact(fi)

    if num != 0:
        num = fact(num)

    ans = num // den

    if k != 0:
        ans = ans * k

    return ans


def canFormPalindrome(s):
    mask = 0

    for ch in s:
        bit = ord(ch) - ord("a")
        mask ^= 1 << bit

    return mask == 0 or (mask & (mask - 1)) == 0


def numofstring(n, m):
    if n == 1:
        return m
    if n == 2:
        return m * (m - 1)
    return m * (m - 1) * pow(m - 2, n - 2)


def longestPalinSubseq(s):
    n = len(s)

    curr = [0] * n
    prev = [0] * n

    for i in range(n - 1, -1, -1):
        curr[i] = 1

        for j in range(i + 1, n):
            if s[i] == s[j]:
                curr[j] = prev[j - 1] + 2
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr[:]
    return curr[n - 1]


def minDeletions(s):
    n = len(s)
    lps = longestPalinSubseq(s)
    return n - lps


def findLongestPalindrome(strr):
    count = [0] * 256
    for i in range(len(strr)):
        count[ord(strr[i])] += 1

    beg = ""
    mid = ""
    end = ""

    ch = ord("a")
    while ch <= ord("z"):
        if count[ch] & 1:
            mid = ch
            count[ch] -= 1
            ch -= 1
        else:
            for i in range(count[ch] // 2):
                beg += chr(ch)
        ch += 1
    end = beg
    end = end[::-1]
    return beg + chr(mid) + end


def cntPalindromes(s, l, r):
    count = 0
    for centre in range(l, r + 1):
        left = centre
        right = centre
        while left >= l and right <= r and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

        left = centre
        right = centre + 1

        while left >= l and right <= r and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count


def substring(s, a, b):
    s1 = ""
    for i in range(a, b, 1):
        s1 += s[i]
    return s1


def allPalindromeSubstring(s):
    v = []
    pivot = 0.0
    while pivot < len(s):
        palindromeRadius = pivot - int(pivot)
        while (
            (pivot + palindromeRadius) < len(s)
            and (pivot - palindromeRadius) >= 0
            and (s[int(pivot - palindromeRadius)] == s[int(pivot + palindromeRadius)])
        ):
            v.append(
                s[int(pivot - palindromeRadius) : int(pivot + palindromeRadius + 1)]
            )
            palindromeRadius += 1
        pivot += 0.5
    return v


def isPalindromePossible(s):
    n = len(s)

    if n == 0:
        return False
    hash = [0] * 26

    for ch in s:
        hash[ord(ch) - ord("a")] += 1

    cnt = 0

    for i in range(26):
        if hash[i] & 1:
            cnt += 1

    if (n & 1) and cnt == 1:
        return True

    if n % 2 == 0 and cnt == 0:
        return True

    return False


def nextPermutation(arr):
    i = len(arr) - 2

    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1

    if i < 0:
        return False

    j = len(arr) - 1

    while arr[j] <= arr[i]:
        j -= 1

    arr[i], arr[j] = arr[i], arr[j]
    left, right = i + 1, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    return True


def allPalindromes(s):
    res = []
    n = len(s)

    if not isPalindromePossible(s):
        return res

    hash = [0] * 26
    half = []
    mid = ""

    for ch in s:
        hash[ord(ch) - ord("a")] += 1

    for i in range(26):
        if hash[i] & 1:
            mid = chr(i + ord("a"))
        half.extend([chr(i + ord("a"))] * (hash[i] // 2))

    while True:
        firstHalf = "".join(half)
        cur = firstHalf

        if n & 1:
            cur += mid

        cur += firstHalf[::-1]

        res.append(cur)

        if not nextPermutation(half):
            break
    return res


def palindrome(s: str, n: int) -> int:
    cnt = dict()
    R = []

    for i in range(n):
        a = s[i]
        if a in cnt:
            cnt[a] += 1
        else:
            cnt[a] = 1

    i = "a"
    while i <= "z":
        if i in cnt and cnt[i] % 2 != 0:
            R += i
        i = chr(ord(i) + 1)
    l = len(R)
    j = 0

    for i in range(l - 1, (l // 2) - 1, -1):
        if R[i] in cnt:
            cnt[R[i]] -= 1
        else:
            cnt[R[i]] = -1

        R[i] = R[j]

        if R[j] in cnt:
            cnt[R[j]] += 1
        else:
            cnt[R[j]] = 1
        j += 1

    first, middle, second = "", "", ""

    i = "a"
    while i <= "z":
        if i in cnt:
            if cnt[i] % 2 == 0:
                j = 0
                while j < cnt[i] // 2:
                    first += i
                    j += 1
            else:
                j = 0
                while j < (cnt[i] - 1) // 2:
                    first += i
                    j += 1

                middle += i
        i = chr(ord(i) + 1)

    second = first
    second = "".join(reverse(second))
    resultant = first + middle + second
    print(resultant)


mem = {}


def process(s, l, r):
    global mem
    ans = 1
    if l > r:
        return 0
    if s[l : r + 1] in mem:
        return mem[s[l : r + 1]]
    for LEN in range(1, (r - l + 1) // 2 + 1, 1):
        if s[l : LEN + 1] == s[r - LEN + 1 : r + 1]:
            ans = max(ans, 2 + process(s, l + LEN, r - LEN))
    mem[s[l : r + 1]] = ans
    return ans


def LPC(s):
    return process(s, 0, len(s) - 1)


def possibility(cnt):
    countodd = 0
    for i in range(10):
        if cnt[i] & 1:
            countodd += 1
    return countodd <= 1


def largestPalindrome(s):
    n = len(s)
    cnt = [0] * 10
    for i in range(n):
        cnt[int(s[i])] += 1

    if not possibility(cnt):
        return ""

    largest = [0] * n
    front = 0

    for i in range(9, -1, -1):
        if cnt[i] & 1:
            largest[n // 2] = i
            cnt[i] -= 1

        while cnt[i] > 0:
            largest[front] = i
            largest[n - front - 1] = i
            cnt[i] -= 2
            front += 1
    return "".join(str(num) for num in largest)


if __name__ == "__main__":
    strr = "geeksforgeeks"
    print(minRemoval(strr))
    s = "geeksgk"
    printPalindromePos(s)
    s = "aaaab"
    if isRotatedPalindrome(s) == True:
        print("true")
    else:
        print("false")
    s = "19495"
    k = 3
    print(maxPalindrome(s, k))
    n = "4697557964"
    result = nextPlain(n)
    print("Input: {}".format(n))
    print("Output: {}".format(result))
    string = "ababab"
    n = len(string)
    print(numberOfPossiblePalindrome(string, n))
    print("True" if canFormPalindrome("geeksgeeks") else False)
    print("True" if canFormPalindrome("geeksforgeeks") else False)
    n = 2
    m = 3
    print(numofstring(n, m))
    s = "aebcdba"
    print(minDeletions(s))
    strr = "abbaccd"
    print(findLongestPalindrome(strr))
    s = "xyaabax"
    l = 3
    r = 5
    print(cntPalindromes(s, l, r))
    v = allPalindromeSubstring("hellolle")
    print(len(v))
    print(v)
    v = allPalindromeSubstring("geeksforgeeks")
    print(len(v))
    print(v)
    s = "abbab"
    res = allPalindromes(s)
    print("[", end="")
    for i in range(len(res)):
        print(res[i], end="")
        if i + 1 < len(res):
            print(", ", end="")
    print("]")
    S = "geeksforgeeks"
    n = len(S)
    palindrome(S, n)
    print(LPC("aaaaabaababbaabaaababababababababbbbaaaaa"))
    s = "313551"
    res = largestPalindrome(s)
    print(res)
