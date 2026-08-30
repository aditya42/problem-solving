def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums[:]
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    ans = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            ans.append(left[i])
            i += 1
        else:
            ans.append(right[j])
            j += 1
    ans.extend(left[i:])
    ans.extend(right[j:])
    return ans


def maximum_subarray_recursive(nums: list[int]) -> int:
    best = cur = nums[0]
    for num in nums[1:]:
        cur = max(num, cur + num)
        best = max(best, cur)
    return best


def generate_parentheses(n: int) -> list[int]:
    ans = []

    def backtrack(opened: int, closed: int, current: list[int]) -> None:
        if len(current) == 2 * n:
            ans.append("".join(current))
            return
        if opened < n:
            current.append("(")
            backtrack(opened + 1, closed, current)
            current.pop()
        if closed < opened:
            current.append(")")
            backtrack(opened, closed + 1, current)
            current.pop()

    backtrack(0, 0, [])
    return ans
