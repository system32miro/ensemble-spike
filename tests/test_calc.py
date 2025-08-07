from src.calc import sum_numbers

def test_sum_basic():
    assert sum_numbers([1, 2, 3]) == 6

def test_sum_empty():
    assert sum_numbers([]) == 0
