from collections import Counter

import math


def maximum_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for value in nums[1:]:
        cur = max(value, value + cur)
        best = max(best, cur)
    return best


def longest_increasing_subsequence(nums: list[int]) -> int:
    tails = []
    for value in nums:
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < value:
                left = mid + 1
            else:
                right = mid
        if left == len(tails):
            tails.append(value)
        else:
            tails[left] = value
    return len(tails)


def coin_change(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return -1 if dp[amount] > amount else dp[amount]


def unique_path(m: int, n: int) -> int:
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]


def minimum_path_sum(grid: list[list[int]]) -> int:
    cols = len(grid[0])
    dp = [math.inf] * cols
    dp[0] = 0
    for row in grid:
        dp[0] += row[0]
        for c in range(1, cols):
            dp[c] = min(dp[c], dp[c - 1]) + row[c]
    return dp[-1]


def longest_common_subsequence(text1: str, text2: str) -> int:
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    prev = [0] * (len(text2) + 1)
    for a in text1:
        cur = [0]
        for j, b in enumerate(text2, 1):
            if a == b:
                cur.append(prev[j - 1] + 1)
            else:
                cur.append(max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def minimum_failing_path_sum(matrix: list[list[int]]) -> int:
    dp = matrix[0][:]
    n = len(matrix)
    for r in range(1, n):
        nxt = [0] * n
        for c in range(n):
            best = dp[c]
            if c:
                best = min(best, dp[c - 1])
            if c + 1 < n:
                best = min(best, dp[c + 1])
            nxt[c] = matrix[r][c] + best
        dp = nxt
    return min(dp)


def zero_one_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)
    return dp[capacity]


def partition_equal_subset_sum(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    possible = {0}
    for value in nums:
        possible |= {
            subtotal + value
            for subtotal in list(possible)
            if subtotal + value <= target
        }
        if target in possible:
            return True
    return False


def predict_the_winner(nums: list[int]) -> bool:
    dp = nums[:]
    n = len(nums)
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            dp[left] = max(nums[left] - dp[left + 1], nums[right] - dp[right])
    return dp[0] >= 0


def split_array_consecutive_subsequences(nums: list[int]) -> bool:
    remaining = Counter(nums)
    tails = Counter()
    for value in nums:
        if remaining[value] == 0:
            continue
        if tails[value - 1] > 0:
            tails[value - 1] -= 1
            tails[value] += 1
        elif remaining[value + 1] > 0 and remaining[value + 2] > 0:
            remaining[value + 1] -= 1
            remaining[value + 2] -= 1
            tails[value + 2] += 1
        else:
            return False
    return True


def max_non_overlapping_subarrays(nums: list[int], target: int) -> int:
    seen = {0}
    prefix = ans = 0
    for value in nums:
        prefix += value
        if prefix - target in seen:
            ans += 1
            seen = {0}
            prefix = 0
        else:
            seen.add(prefix)
    return ans


def partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    ans = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            ans.append(end - start + 1)
            start = i + 1
    return ans


def subarray_sums_divisible_by_k(nums: list[int], k: int) -> int:
    mods = Counter({0: 1})
    prefix = ans = 0
    for value in nums:
        prefix = (prefix + value) % k
        ans += mods[prefix]
        mods[prefix] += 1
    return ans


def count_numbers_with_unique_digits(n: int) -> int:
    if n == 0:
        return 1
    n = min(n, 10)
    ans = 10
    unique = 9
    available = 9
    for _ in range(2, n + 1):
        unique *= available
        ans += unique
        available -= 1
    return ans


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    prefix = Counter({0: 1})
    running = ans = 0
    for value in nums:
        running += value
        ans += prefix[running - k]
        prefix[running] += 1
    return ans


def target_sum_ways(nums: list[int], target: int) -> int:
    ways = Counter({0: 1})
    for value in nums:
        nxt = Counter()
        for subtotal, count in ways.items():
            nxt[subtotal + value] += count
            nxt[subtotal - value] += count
        ways = nxt
    return ways[target]
