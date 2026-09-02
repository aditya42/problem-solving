import csv
import re
from collections import Counter
from itertools import zip_longest

WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['`][^\W\d_]+)*", re.UNICODE)

def word_frequency(text: str) -> dict[str, int]:
    normalized = text.casefold()

    words = (match.group(0) for match in WORD_PATTERN.finditer(normalized))

    counts = Counter(words)

    return dict(counts)


def compare_translation_results(
    expected: list[tuple[str, str]], actual: list[tuple[str, str]]
) -> dict:
    missing = object()

    passed = 0
    failed = 0
    failures = []

    pairs = zip_longest(expected, actual, fillvalue=missing)

    for index, (expected_item, actual_item) in enumerate(pairs):
        if expected_item is missing:
            failed += 1
            failures.append(
                {
                    "index": index,
                    "reason": "unexpected actual result",
                    "expected": None,
                    "actual": actual_item,
                }
            )
            continue

        if actual_item is missing:
            failed += 1
            failures.append(
                {
                    "index": index,
                    "reason": "missing actual result",
                    "expected": expected_item,
                    "actual": None,
                }
            )
            continue

        expected_source, expected_translation = expected_item
        actual_source, actual_translation = actual_item

        if (
            expected_source == actual_source
            and expected_translation == actual_translation
        ):
            passed += 1
        else:
            failed += 1
            failures.append(
                {
                    "index": index,
                    "source": expected_source,
                    "expected": expected_translation,
                    "actual": actual_translation,
                }
            )
    return {
        "total": passed + failed,
        "passed": passed,
        "failed": failed,
        "failures": failures,
    }


def detect_regressions(
    old_scores: dict[str, float],
    new_scores: dict[str, float],
    threshold_percent: float = 5.0,
) -> list[dict]:

    regressions = []

    for language_pair, old_score in old_scores.items():
        if language_pair not in new_scores:
            continue

        new_score = new_scores[language_pair]

        if old_score <= 0:
            continue

        decrease = old_score - new_score

        if decrease <= 0:
            continue

        decrease_percent = (decrease / old_score) * 100

        if decrease_percent > threshold_percent:
            regressions.append(
                {
                    "language_pair": language_pair,
                    "old_score": old_score,
                    "new_score": new_score,
                    "decrease_percent": decrease_percent,
                }
            )
    return regressions


def parse_mt_logs(lines: list[str]) -> dict:
    total = 0
    passed = 0
    failed = 0
    malformed = 0
    latency_sum = 0
    failures_by_language = Counter()

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        fields = line.split("|")

        if len(fields) != 4:
            malformed += 1
            continue

        status, language, client, latency_text = fields

        try:
            latency = int(latency_text)
        except ValueError:
            malformed += 1
            continue

        if status not in {"PASS", "FAIL"}:
            malformed += 1
            continue

        if latency < 0:
            malformed += 1
            continue

        total += 1
        latency_sum += latency

        if status == "PASS":
            passed += 1
        else:
            failed += 1
            failures_by_language[language] += 1

    average_latency = latency_sum / total if total else 0.0

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "malformed": malformed,
        "failure_by_languages": dict(failures_by_language),
        "average_latency_ms": average_latency,
    }


def translation_accuracy(reference: list[str], prediction: list[str]) -> float:
    if len(reference) != len(prediction):
        raise ValueError("Reference and prediction sizes must match")
    if not reference:
        return 0.0

    matches = 0

    for expected, actual in zip(reference, prediction):
        if expected == actual:
            matches += 1

    accuracy = (matches / len(reference)) * 100

    return accuracy


def compare_translation_files(
    source_path: str,
    reference_path: str,
    candidate_path: str,
    report_path: str,
) -> dict:
    missing = object()

    total_records = 0
    compared_records = 0
    passed = 0
    failed = 0
    malformed = 0

    with (
        open(source_path, "r", encoding="utf-8") as source_file,
        open(reference_path, "r", encoding="utf-8") as reference_file,
        open(candidate_path, "r", encoding="utf-8") as candidate_file,
        open(
            report_path,
            "r",
            encoding="utf-8",
            newline="",
        ) as report_file,
    ):
        writer = csv.writer(
            report_file,
            delimiter="\t",
        )

        writer.writerow(["line", "status", "source", "reference", "candidate"])

        rows = zip_longest(
            source_file, reference_file, candidate_file, fillvalue=missing
        )

        for line_number, row in enumerate(rows, start=1):
            total_records += 1

            source_line, reference_line, candidate_line = row

            if any(value in missing for value in row):
                malformed += 1

                writer.writerow(
                    [
                        line_number,
                        "MALFORMED",
                        "" if source_line is missing else source_line.rstrip("\r\n"),
                        ""
                        if reference_line is missing
                        else reference_line.rstrip("\r\n"),
                        ""
                        if candidate_line is missing
                        else candidate_line.rstrip("\r\n"),
                    ]
                )

                continue

            source = source_line.rstrip("\r\n")
            reference = reference_line.rstrip("\r\n")
            candidate = candidate_line.rstrip("\r\n")

            compared_records += 1

            if reference == candidate:
                passed += 1
            else:
                failed += 1

                writer.writerow(
                    [
                        line_number,
                        "MISMATCH",
                        source,
                        reference,
                        candidate,
                    ]
                )

    accuracy = passed / compared_records * 100 if compared_records else 0.0

    return {
        "total_records": total_records,
        "compared_records": compared_records,
        "passed": passed,
        "failed": failed,
        "malformed": malformed,
        "accuracy_present": accuracy,
    }


def longest_common_prefix(strings: list[str]) -> str:
    if not strings:
        return ""

    shortest = min(strings, key=len)

    for index, character in enumerate(shortest):
        for current_string in strings:
            if current_string[index] != character:
                return shortest[:index]

    return shortest


def first_unique_character(text: str) -> str:
    counts = Counter(text)

    for character in text:
        if counts[character] == 1:
            return character

    return ""


import unicodedata


def normalize_text(text: str, remove_accents: bool = False) -> str:
    text = unicodedata.normalize("NFKC", text)

    text = text.casefold()

    if remove_accents:
        text = unicodedata.normalize("NFKD", text)

        text = "".join(
            character for character in text if not unicodedata.combining(character)
        )

    normalized_characters = []

    for character in text:
        category = unicodedata.category(character)

        if category.startswith("P"):
            normalized_characters.append(" ")
        else:
            normalized_characters.append(character)

    cleaned = "".join(normalized_characters)

    cleaned = "".join(cleaned.split())

    cleaned = unicodedata.normalize("NFC", cleaned)

    return cleaned


def equivalent_text(first: str, second: str, remove_accents: bool = False) -> bool:

    return normalize_text(first, remove_accents) == normalize_text(
        second, remove_accents
    )


def find_duplicate_tests(
    test_cases: list[tuple[str, str]],
) -> list[tuple[str, str]]:

    seen = set()
    emitted = set()
    duplicates = []

    for test_case in test_cases:
        if test_case not in seen:
            seen.add(test_case)
            continue
        if test_case not in emitted:
            duplicates.append(test_case)
            emitted.add(test_case)

    return duplicates


if __name__ == "__main__":
    tests = [
        ("hello", "fr"),
        ("goodbye", "de"),
        ("hello", "fr"),
        ("welcome", "ja"),
    ]

    assert find_duplicate_tests(tests) == [("hello", "fr")]

    assert equivalent_text("Hello, World! ", "hello world")

    assert first_unique_character("leetcode") == "l"

    assert (
        longest_common_prefix(["translate", "translation", "translator"]) == "translat"
    )

    assert word_frequency("Hello, hello! HELLO?") == {"hello": 3}

    expected = [
        ("hello", "bonjour"),
        ("goodbye", "au revoir"),
    ]

    actual = [
        ("hello", "bonjour"),
        ("goodbye", "adieu"),
    ]

    result = compare_translation_results(expected, actual)

    assert result["total"] == 2
    assert result["passed"] == 1
    assert result["failed"] == 1
    assert result["failures"][0]["source"] == "goodbye"

    old_scores = {
        "en-fr": 0.91,
        "en-de": 0.88,
        "en-ja": 0.90,
    }

    new_scores = {
        "en-fr": 0.92,
        "en-de": 0.80,
        "en-ja": 0.89,
    }

    result = detect_regressions(old_scores, new_scores)

    assert len(result) == 1
    assert result[0]["language_pair"] == "en-de"
    assert round(result[0]["decrease_percent"], 2) == 9.09

    logs = [
        "PASS|en-fr|TranslateApp|120",
        "FAIL|en-de|Safari|340",
        "PASS|en-ja|TranslateApp|180",
        "FAIL|en-de|TranslateApp|290",
    ]

    result = parse_mt_logs(logs)

    assert result["total"] == 4
    assert result["passed"] == 2
    assert result["failed"] == 2
    assert result["failures_by_language"] == {"en-de": 2}
    assert result["average_latency_ms"] == 232.5

    result = parse_mt_logs(
        ["PASS|en-fr|TranslateApp|100", "INVALID RECORD", "FAIL|en-de|Safari|abc"]
    )

    assert result["total"] == 1
    assert result["malformed"] == 2

    reference = [
        "hello",
        "world",
        "apple",
    ]

    prediction = [
        "hello",
        "earth",
        "apple",
    ]

    assert round(translation_accuracy(reference, prediction), 2) == 66.67

    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)

        source = directory / "source.text"
        reference = directory / "reference.txt"
        candidate = (directory / "candidate.txt",)
        report = directory / "report.tsv"

        source.write_text("hello\ngoodbye\nwelcome\n", encoding="utf-8")

        reference.write_text("bonjour\nau revoir\nbienvenue\n", encoding="utf-8")

        candidate.write_text("bonjour\nadieu\nbienvenue\n", encoding="utf-8")

        result = compare_translation_files(
            str(source), str(reference), str(candidate), str(report)
        )

        assert result["total_records"] == 3
        assert result["passed"] == 2
        assert result["failed"] == 1
        assert result["malformed"] == 0
        assert round(result["accuracy_present"], 2) == 66.67
