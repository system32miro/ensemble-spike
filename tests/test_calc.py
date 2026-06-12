from src.calc import sum_numbers, multiply_numbers

# ── sum_numbers ──────────────────────────────────────────────────────

def test_sum_basic():
    assert sum_numbers([1, 2, 3]) == 6

def test_sum_empty():
    assert sum_numbers([]) == 0

def test_sum_mixed_types():
    assert sum_numbers([1, 2.5, None, "3", 4]) == 7.5

def test_sum_all_floats():
    assert sum_numbers([1.5, 2.5]) == 4.0

# ── multiply_numbers ─────────────────────────────────────────────────

def test_multiply_basic():
    assert multiply_numbers([2, 3, 4]) == 24

def test_multiply_empty():
    assert multiply_numbers([]) == 0

def test_multiply_mixed_types():
    assert multiply_numbers([2, 3.0, None, "x", 0.5]) == 3.0
