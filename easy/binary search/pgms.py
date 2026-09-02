def search_insert_position(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while right > left:
        mid = (left + right) // 2
        if target > nums[mid]:
            left = mid + 1
        else:
            right = mid
    return left


def next_greatest_letter(letters: list[str], target: str) -> str:
    left, right = 0, len(letters)
    while right > left:
        mid = (left + right) // 2
        if target > letters[mid]:
            left = mid + 1
        else:
            right = mid
    return letters[left % len(letters)]


def find_max_average(nums: list[int], k: int) -> float:
    cur = sum(nums[:k])
    best = cur
    for i in range(k, len(nums)):
        cur += nums[i] - nums[i - k]
        best = max(best, cur)
    return best / k


def valid_perfect_square(num: int) -> bool:
    if num < 2:
        return True
    left, right = 1, num // 2
    while right >= left:
        mid = (left + right) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            left = mid + 1
        else:
            right = mid - 1
    return False


def count_negatives_sorted_matrix(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    r, c = rows - 1, 0
    count = 0
    while r >= 0 and cols > c:
        if grid[r][c] < 0:
            count += cols - c
            r -= 1
        else:
            c += 1
    return count
