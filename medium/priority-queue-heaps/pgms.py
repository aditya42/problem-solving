import heapq
from collections import Counter


def kth_largest_element(nums: list[int], k: int) -> int:
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def top_k_frequent_elements(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)
    ans = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            ans.append(value)
            if len(ans) == k:
                return ans
    return ans


def kth_smallest_matrix_heap(matrix: list[list[int]], k: int) -> int:
    heap = []
    for r in range(min(len(matrix), k)):
        heapq.heappush(heap, (matrix[r][0], r, 0))
    value = 0
    for _ in range(k):
        value, r, c = heapq.heappop(heap)
        if c + 1 < len(matrix[r]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return value


def frequency_sort(s: str) -> str:
    counts = Counter(s)
    return "".join(ch * freq for ch, freq in counts.most_common())


def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    return sorted(counts, key=lambda word: (-counts[word], word))[:k]


def k_closest_points(points: list[list[int]], k: int) -> list[list[int]]:
    heap = []
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]


def top_k_frequent_elements_sorted_matrix(matrix: list[list[int]], k: int) -> list[int]:
    counts = Counter(value for row in matrix for value in row)
    return [value for value, _ in counts.most_common()]


def maximum_sum_subarray_size_k(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    current = sum(nums[:k])
    best = current
    for i in range(k, len(nums)):
        current += nums[i] - nums[i - k]
        best = max(best, current)
    return best


def find_smallest_common_number(a: list[int], b: list[int], c: list[int]) -> int:
    i = j = k = 0
    while i < len(a) and j < len(b) and k < len(c):
        if a[i] == b[j] == c[k]:
            return a[i]
        minimum = min(a[i], b[j], c[k])
        if a[i] == minimum:
            i += 1
        if b[j] == minimum:
            j += 1
        if c[k] == minimum:
            k += 1
    return -1


def longest_ones_after_k_flips(nums: list[int], k: int) -> int:
    left = zeros = best = 0
    for right, value in enumerate(nums):
        if value == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
