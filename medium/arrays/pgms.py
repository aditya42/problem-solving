import heapq
import math
from functools import cmp_to_key


def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    ans = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                ans.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return ans


def find_duplicates(nums: list[int]) -> list[int]:
    ans = []
    for value in nums:
        idx = abs(value) - 1
        if nums[idx] < 0:
            ans.append(abs(value))
        else:
            nums[idx] *= -1
    return ans


def num_subarray_product_less_than_k(nums: list[int], k: int):
    if k <= 1:
        return 0
    product = 1
    left = ans = 0
    for right, value in enumerate(nums):
        product *= value
        while product >= k:
            product /= nums[left]
            left += 1
        ans += right - left + 1
    return ans


class NumArrayMutable:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.values = [0] * self.n
        self.tree = [0] * (self.n + 1)
        for i, value in enumerate(nums):
            self.update(i, value)

    def update(self, index: int, value: int) -> None:
        delta = value - self.values[index]
        self.values[index] = value
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def _prefix(self, index: int) -> int:
        total = 0
        i = index + 1
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right) - self._prefix(left - 1)


def max_score_cards(card_points: list[int], k: int) -> int:
    n = len(card_points)
    if k == n:
        return sum(card_points)
    keep = n - k
    cur = sum(card_points[:keep])
    min_keep = cur
    for right in range(keep, n):
        cur += card_points[right] - card_points[right - keep]
        min_keep = min(min_keep, cur)
    return sum(card_points) - min_keep


def three_sum_closest(nums: list[int], target: int) -> int:
    nums.sort()
    closest = sum(nums[:3])
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if abs(total - target) < abs(closest - target):
                closest = total
            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                return target
    return closest


def minimum_window_sort(nums: list[int]) -> int:
    n = len(nums)
    if n < 2:
        return 0
    left = 0
    while left < n - 1 and nums[left] <= nums[left + 1]:
        left += 1
    if left == n - 1:
        return 0
    right = n - 1
    while right > 0 and nums[right] >= nums[right - 1]:
        right -= 1
    wmin = min(nums[left : right + 1])
    wmax = max(nums[left : right + 1])
    while left > 0 and nums[left - 1] > wmin:
        left -= 1
    while right < n - 1 and nums[right + 1] < wmax:
        right += 1
    return right - left + 1


def sort_colors(nums: list[int]) -> None:
    low = cur = 0
    high = len(nums) - 1
    while cur <= high:
        if nums[cur] == 0:
            nums[low], nums[cur] = nums[cur], nums[low]
            low += 1
            cur += 1
        elif nums[cur] == 1:
            cur += 1
        else:
            nums[cur], nums[high] = nums[high], nums[cur]
            high -= 1


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    ans = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1], end)
        else:
            ans.append([start, end])
    return ans


def wiggle_sort_ii(nums: list[int]) -> None:
    ordered = sorted(nums)
    mid = (len(nums) - 1) // 2
    nums[::2] = ordered[: mid + 1][::-1]
    nums[1::2] = ordered[mid + 1 :][::-1]


def largest_number(nums: list[int]) -> str:
    values = list(map(str, nums))

    def cmp(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    values.sort(key=cmp_to_key(cmp))
    return "0" if values and values[0] == "0" else "".join(values)


def longest_mountain(arr: list[int]) -> int:
    up = down = best = 0
    for i in range(1, len(arr)):
        if (down and arr[i] > arr[i - 1]) or arr[i] == arr[i - 1]:
            up = down = 0
        if arr[i] > arr[i - 1]:
            up += 1
        elif arr[i] < arr[i - 1]:
            down += 1
        if up and down:
            best = max(best, up + down + 1)
    return best


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort()
    heap = []
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)


def min_subarray_len(target: int, nums: list[int]) -> int:
    left = total = 0
    best = math.inf
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == math.inf else best


def interval_intersection(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    i = j = 0
    ans = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            ans.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return ans


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    removed = 0
    end = intervals[0][1]
    for start, nxt_end in intervals[1:]:
        if start < end:
            removed += 1
        else:
            end = nxt_end
    return removed


def insert_intervals(
    intervals: list[list[int]], new_interval: list[int]
) -> list[list[int]]:
    ans, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new_interval[0]:
        ans.append(intervals[i])
        i += 1
    start, end = new_interval
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    ans.append([start, end])
    ans.extend(intervals[i:])
    return ans
