import math
from typing import Iterable, TypedDict


class NumberSummary(TypedDict):
    count: int
    total: int | float
    minimum: int | float | None
    maximum: int | float | None
    average: float | None
    values: list[int | float]


def summarize_numbers(values: Iterable[object]) -> NumberSummary:
    numeric_values: list[int | float] = []
    total = 0
    minimum = None
    maximum = None

    for value in values:
        if not _is_supported_number(value):
            continue
        numeric_values.append(value)
        total += value
        minimum = value if minimum is None else min(minimum, value)
        maximum = value if maximum is None else max(maximum, value)

    count = len(numeric_values)

    return {
        "count": count,
        "total": total,
        "minimum": minimum,
        "maximum": maximum,
        "average": total / count if count else None,
        "values": numeric_values,
    }


def _is_supported_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
