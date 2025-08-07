from typing import Iterable, Union

Number = Union[int, float]

def sum_numbers(values: Iterable[Number]) -> Number:
    total = 0
    for v in values:
        if isinstance(v, (int, float)):
            total += v
    return total
