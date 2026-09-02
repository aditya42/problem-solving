from collections import Counter, defaultdict


def daily_temperature(temperatures: list[int]) -> list[int]:
    ans = [0] * len(temperatures)
    stack = []
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


def remove_duplicate_letters(s: str) -> str:
    remaining = Counter(s)
    stack = []
    in_stack = set()
    for ch in s:
        remaining[ch] -= 1
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and remaining[stack[-1]] > 0:
            in_stack.remove(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)


def basic_calculator_ii(s: str) -> int:
    stack = []
    number = 0
    operation = "+"
    for i, ch in enumerate(s):
        if ch.isdigit():
            number = number * 10 + int(ch)
        if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
            if operation == "+":
                stack.append(number)
            elif operation == "-":
                stack.append(-number)
            elif operation == "*":
                stack.append(stack.pop() * number)
            else:
                previous = stack.pop()
                stack.append(int(previous / number))
            operation = ch
            number = 0
    return sum(stack)


def evaluate_reverse_polish_notation(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token not in {"+", "-", "*", "/"}:
            stack.append(int(token))
            continue
        b = stack.pop()
        a = stack.pop()
        if token == "+":
            stack.append(a + b)
        elif token == "-":
            stack.append(a - b)
        elif token == "*":
            stack.append(a * b)
        else:
            stack.append(int(a / b))
    return stack[-1]


def evaluate_division(
    equations: list[list[str]], values: list[float], queries: list[list[str]]
) -> list[float]:
    graph = defaultdict(list)
    for (a, b), value in zip(equations, values):
        graph[a].append((b, value))
        graph[b].append((a, 1 / value))

    def dfs(source: str, target: str, seen: set[str]) -> float:
        if source not in graph or target not in graph:
            return -1.0
        if source == target:
            return 1.0
        seen.add(source)
        for nxt, weight in graph[source]:
            if nxt not in seen:
                result = dfs(nxt, target, seen)
                if result != 1.0:
                    return weight * result
        return -1.0

    return [dfs(a, b, set()) for s, b in queries]


def simplify_path(path: str):
    stack = []
    for part in path.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)
