from collections import Counter, defaultdict


def find_failure_dependencies(failed_tests, test_dependencies):

    dependency_failures = Counter()

    for test in failed_tests:
        dependencies = test_dependencies.get(test, [])

        for dependency in dependencies:
            dependency_failures[dependency] += 1

    return dependency_failures.most_common()


def dependency_failure_scores(failed_tests, test_dependencies):
    failed_tests = set(failed_tests)

    total_usage = defaultdict(int)

    failed_usage = defaultdict(int)

    for test, dependencies in test_dependencies.items():
        for dependency in dependencies:
            total_usage[dependency] += 1

            if test in failed_tests:
                failed_usage[dependency] += 1
    scores = []

    for dependency, failed_count in failed_usage.items():
        total_count = total_usage[dependency]

        score = failed_count / total_count

        scores.append((dependency, failed_count, total_count, score))

    return sorted(scores, key=lambda x: (x[3], x[1]), reverse=True)


test_dependencies = {
    "test_checkout": ["payment", "inventory", "cart"],
    "test_refund": ["payment", "orders"],
    "test_add_card": ["payment"],
    "test_search": ["search"],
    "test_cart": ["cart", "inventory"],
}


failed_tests = ["test_checkout", "test_refund", "test_add_card"]


print(find_failure_dependencies(failed_tests, test_dependencies))

print(dependency_failure_scores(failed_tests, test_dependencies))
