from collections import defaultdict
from io import StringIO


def find_flaky_tests(file_obj):
    status_map = defaultdict(int)

    for line in file_obj:
        line = line.strip()

        if not line:
            continue

        test_name, status = line.split(",", 1)

        status = status.strip().upper()

        if status == "PASS":
            status_map[test_name] |= 1

        elif status == "FAIL":
            status_map[test_name] |= 2

    flaky_tests = [test_name for test_name, mask in status_map.items() if mask == 3]

    return flaky_tests


data = StringIO(
    """test_login,PASS
test_checkout,FAIL
test_login,FAIL
test_search,PASS
test_checkout,FAIL
test_payment,PASS
test_payment,FAIL
test_payment,FAIL
test_payment,PASS
"""
)

print(find_flaky_tests(data))
