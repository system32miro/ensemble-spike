from typing import Iterable, Union

Number = Union[int, float]


def summarize_numbers(values: Iterable[object]) -> dict[str, object]:
    numeric_values = [value for value in values if _is_supported_number(value)]
    total = sum(numeric_values)
    count = len(numeric_values)

    return {
        "count": count,
        "total": total,
        "minimum": min(numeric_values) if numeric_values else None,
        "maximum": max(numeric_values) if numeric_values else None,
        "average": total / count if numeric_values else None,
        "values": numeric_values,
    }


def _is_supported_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
