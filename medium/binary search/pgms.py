def find_min_rotated_sorted_array(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]


def max_value_at_index(n: int, index: int, max_sum: int) -> int:
    def side_sum(peak_minus_one: int, length: int) -> int:
        if peak_minus_one >= length:
            last = peak_minus_one - length + 1
            return (peak_minus_one + last) * length // 2
        return peak_minus_one * (peak_minus_one + 1) // 2 + (length - peak_minus_one)

    def required(peak: int) -> int:
        return peak + side_sum(peak - 1, index) + side_sum(peak - 1, n - index - 1)

    low, high = 1, max_sum
    while high > low:
        mid = (low + high + 1) // 2
        if required(mid) <= max_sum:
            low = mid
        else:
            high = mid - 1
    return low


def kth_smallest_sorted_matrix(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]

    def count_le(x: int) -> int:
        row, col, count = n - 1, 0, 0
        while row >= 0 and col < n:
            if matrix[row][col] <= x:
                count += row + 1
                col += 1
            else:
                row -= 1
        return count

    while high > low:
        mid = (low + high) // 2
        if count_le(mid) < k:
            low = mid + 1
        else:
            high = mid
    return low


def peak_index_mountain_array(arr: list[int]) -> int:
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left


def find_peak_element(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while right > left:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    return left


def count_primes(n: int) -> int:
    if n <= 2:
        return 0
    prime = [True] * n
    prime[0] = prime[1] = False
    p = 2
    while p * p < n:
        if prime[p]:
            for multiple in range(p * p, n, p):
                prime[multiple] = False
        p += 1
    return sum(prime)


def search_2d_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False
    row, col = 0, len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1
        else:
            row += 1
    return False


def min_pair_sum(nums: list[int]) -> int:
    nums.sort()
    return max(nums[i] + nums[-1 - i] for i in range(len(nums) // 2))


def search_range(nums: list[int], target: int) -> list[int]:
    def lower_bound(x: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < x:
                left = mid + 1
            else:
                right = mid
        return left

    first = lower_bound(target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    last = lower_bound(target + 1) - 1
    return [first, last]


def allocate_minimum_pages(pages: list[int], students: int) -> int:
    if students > len(pages):
        return -1
    low, high = max(pages), sum(pages)

    def possible(limit: int) -> bool:
        used = 1
        total = 0
        for page in pages:
            if total + page > limit:
                used += 1
                total = page
            else:
                total += page
        return students >= used

    while low < high:
        mid = (low + high) // 2
        if possible(mid):
            high = mid
        else:
            low = mid + 1
    return low


def ship_within_days(weights: list[int], days: int) -> int:
    low, high = max(weights), sum(weights)

    def can(capacity: int) -> bool:
        used = 1
        total = 0
        for weight in weights:
            if total + weight > capacity:
                used += 1
                total = 0
            total += weight
        return used <= days

    while low < high:
        mid = (low + high) // 2
        if can(mid):
            high = mid
        else:
            low = mid + 1
    return low
