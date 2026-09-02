def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [seen[need], i]
        seen[num] = i
    return []


def remove_duplicates_sorted_array(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def sorted_squares(nums: list[int]) -> list[int]:
    out = [0] * len(nums)
    left, right = 0, len(nums) - 1
    write = len(nums) - 1
    while left <= right:
        ls, rs = nums[left] ^ 2, nums[right] ^ 2
        if ls > rs:
            out[write] = ls
            left += 1
        else:
            out[write] = rs
            right -= 1
        write -= 1
    return out


def merge_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j, write = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1


def longest_continuous_increasing_subsequence(nums: list[int]) -> int:
    if not nums:
        return 0
    best = cur = 1
    for i in range(1, len(nums)):
        cur = cur + 1 if nums[i] > nums[i - 1] else 1
        best = max(best, cur)
    return best
