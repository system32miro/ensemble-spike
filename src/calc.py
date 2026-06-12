from typing import Iterable, Union

Number = Union[int, float]


def sum_numbers(values: Iterable[Number]) -> Number:
    """Sum all numeric values in an iterable, skipping non-numeric items."""
    total = 0.0
    for v in values:
        if isinstance(v, (int, float)):
            total += v
    return int(total) if total == int(total) else total


def multiply_numbers(values: Iterable[Number]) -> Number:
    """Multiply all numeric values in an iterable, skipping non-numeric items."""
    product = 1.0
    found = False
    for v in values:
        if isinstance(v, (int, float)):
            product *= v
            found = True
    if not found:
        return 0
    return int(product) if product == int(product) else product
