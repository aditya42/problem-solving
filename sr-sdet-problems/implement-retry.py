import time
import random
from functools import wraps


def retry(max_attempt=3, initial_delay=1, max_delay=30, expections=(Exception,)):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwrgs):
            delay = initial_delay

            for attempt in range(1, max_attempt + 1):
                try:
                    return func(*args, **kwrgs)
                except expections:
                    if attempt == max_attempt:
                        raise
                    jitter = random.uniform(0, delay * 0.1)

                    sleep_time = delay + jitter

                    print(f"Attempt {attempt} failed. Retrying in {sleep_time:.2f}s")

                    time.sleep(sleep_time)

                    delay = min(delay * 2, max_delay)

        return wrapper

    return decorator


counter = 0


@retry(max_attempt=4, initial_delay=1, expections=(ConnectionError,))
def call_service():

    global counter

    counter += 1

    print("API attempt:", counter)

    if counter < 3:
        raise ConnectionError("Service unavailable")

    return "Success"


print(call_service())
