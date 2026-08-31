import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

        def add(self, val: int) -> int:
            if len(self.heap) < self.k:
                heapq.heappush(self.heap, val)
            elif val > self.heap[0]:
                heapq.heapreplace(self.heap, val)
            return self.heap[0]


def merger_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int):
    i, j, write = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1


def merger_sorted_array_heap_section(
    num1: list[int], m: int, nums2: list[int], n: int
) -> None:
    merger_sorted_array(num1, m, nums2, n)
