from src.calc import sum_numbers

def test_sum_basic():
    assert sum_numbers([1, 2, 3]) == 6

def test_sum_empty():
    assert sum_numbers([]) == 0

def test_sum_mixed_types():
    assert sum_numbers([1, 2.5, None, "3", 4]) == 7.5
