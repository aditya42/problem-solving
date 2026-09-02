from functools import lru_cache


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is undefined for negative integers")
    return 1 if n <= 1 else n * factorial(n - 1)


def recursive_binary_search(nums: list[int], target: int) -> int:
    def search(left: int, right: int) -> int:
        if left > right:
            return -1
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return search(mid + 1, right)
        return search(left, mid - 1)

    return search(0, len(nums) - 1)


def fibonacci_recursive(n: int) -> int:
    @lru_cache(None)
    def fib(x: int) -> int:
        if x <= 1:
            return x
        return fib(x - 1) + fib(x - 2)

    return fib(n)
