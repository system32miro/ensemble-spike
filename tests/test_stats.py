import math

from src.stats import summarize_numbers


def test_summarize_numbers_reports_basic_metrics():
    summary = summarize_numbers([1, 2.5, 4])

    assert summary["count"] == 3
    assert summary["total"] == 7.5
    assert summary["minimum"] == 1
    assert summary["maximum"] == 4
    assert summary["average"] == 2.5
    assert summary["values"] == [1, 2.5, 4]


def test_summarize_numbers_filters_unsupported_values():
    summary = summarize_numbers([1, True, None, "2", object(), 3])

    assert summary["count"] == 2
    assert summary["total"] == 4
    assert summary["minimum"] == 1
    assert summary["maximum"] == 3
    assert summary["average"] == 2
    assert summary["values"] == [1, 3]


def test_summarize_numbers_handles_empty_or_non_numeric_input():
    summary = summarize_numbers([None, False, "skip"])

    assert summary["count"] == 0
    assert summary["total"] == 0
    assert summary["minimum"] is None
    assert summary["maximum"] is None
    assert summary["average"] is None
    assert summary["values"] == []


def test_summarize_numbers_filters_non_finite_values():
    summary = summarize_numbers([1, math.nan, 2, math.inf, -math.inf, 3])

    assert summary["count"] == 3
    assert summary["total"] == 6
    assert summary["minimum"] == 1
    assert summary["maximum"] == 3
    assert summary["average"] == 2
    assert summary["values"] == [1, 2, 3]


def test_summarize_numbers_supports_negative_and_large_values():
    large = 10**18
    summary = summarize_numbers([-10, large, 5])

    assert summary["count"] == 3
    assert summary["total"] == large - 5
    assert summary["minimum"] == -10
    assert summary["maximum"] == large
    assert summary["average"] == (large - 5) / 3
    assert summary["values"] == [-10, large, 5]
