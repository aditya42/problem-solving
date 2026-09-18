from queue import Queue, Empty
from contextlib import contextmanager


class ResourcePool:
    def __init__(self, resources):
        self.pool = Queue()

        for resource in resources:
            self.pool.put(resource)

    def acquire(self, timeout=None):

        try:
            return self.pool.get(timeout=timeout)
        except Empty:
            raise TimeoutError("No resource available")

    def release(self, resource):
        self.pool.put(resource)

    @contextmanager
    def resource(self, timeout=None):
        device = self.acquire(timeout)

        try:
            yield device
        finally:
            self.release(device)


import threading
import time

devices = ["iPhone-15", "iPhone-16", "Pixel-9"]

pool = ResourcePool(devices)


def run_test(test_name):

    with pool.resource(timeout=5) as device:
        print(f"{test_name} started on {device}")

        time.sleep(1)

        print(f"{test_name} finished on {device}")


threads = []

for i in range(5):
    thread = threading.Thread(target=run_test, args=(f"test_{i}",))
    threads.append(thread)

    thread.start()

for thread in threads:
    thread.join()
