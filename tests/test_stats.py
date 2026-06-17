from src.stats import summarize_numbers


def test_summarize_numbers_returns_core_metrics():
    summary = summarize_numbers([4, 8, 15, 16, 23, 42])

    assert summary["count"] == 6
    assert summary["total"] == 108
    assert summary["minimum"] == 4
    assert summary["maximum"] == 42
    assert summary["average"] == 18
    assert summary["values"] == [4, 8, 15, 16, 23, 42]


def test_summarize_numbers_ignores_non_numeric_values_and_booleans():
    summary = summarize_numbers([1, None, "2", True, False, 3.5, object()])

    assert summary["count"] == 2
    assert summary["total"] == 4.5
    assert summary["minimum"] == 1
    assert summary["maximum"] == 3.5
    assert summary["average"] == 2.25
    assert summary["values"] == [1, 3.5]


def test_summarize_numbers_handles_empty_or_non_numeric_input():
    summary = summarize_numbers([None, "skip", False])

    assert summary["count"] == 0
    assert summary["total"] == 0
    assert summary["minimum"] is None
    assert summary["maximum"] is None
    assert summary["average"] is None
    assert summary["values"] == []
