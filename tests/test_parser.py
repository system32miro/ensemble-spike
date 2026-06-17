import pytest
from src.parser import evaluate_expression, average, running_max


def test_evaluate_expression():
    assert evaluate_expression("1 + 2 * 3") == 7


def test_evaluate_rejects_unsafe():
    with pytest.raises(ValueError):
        evaluate_expression("__import__('os').system('echo hi')")


def test_average():
    assert average([1, 2, 3]) == 2.0
    assert average([]) == 0.0


def test_running_max_negative():
    assert running_max([-5, -3, -1]) == -1
