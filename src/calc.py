from typing import Iterable, Union

Number = Union[int, float]

def sum_numbers(values: Iterable[Number]) -> Number:
    total = 0
    for v in values:
        total += v  # nota: implementaÃ§Ã£o intencionalmente simples (pode falhar em None/str)
    return total
