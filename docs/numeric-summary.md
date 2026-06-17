# Numeric summary helper

`src.stats.summarize_numbers` turns a mixed iterable into a compact metrics
payload. It is intentionally small because this repository is a spike, but the
helper documents the rules that future agents should preserve when extending the
calculation surface.

## Inputs

The function accepts any iterable. Each item is inspected independently:

- `int` values are included.
- `float` values are included.
- `NaN`, `Infinity`, and `-Infinity` are ignored.
- `bool` values are ignored even though Python treats `bool` as an `int`
  subclass.
- strings, `None`, objects, and other unsupported values are ignored.

This extends the lightweight filtering approach used by `sum_numbers` with
stricter rules for booleans and non-finite numbers, so callers do not
accidentally count flags or poison summary metrics with IEEE 754 sentinel values.

## Output shape

The function returns a dictionary with these keys:

| Key | Meaning |
| --- | --- |
| `count` | Number of accepted numeric values. |
| `total` | Sum of accepted numeric values. |
| `minimum` | Lowest accepted numeric value, or `None` when there are no values. |
| `maximum` | Highest accepted numeric value, or `None` when there are no values. |
| `average` | Arithmetic mean, or `None` when there are no values. |
| `values` | Accepted values in their original order. |

## Example

```python
from src.stats import summarize_numbers

summary = summarize_numbers([1, None, "2", True, 3.5])

assert summary == {
    "count": 2,
    "total": 4.5,
    "minimum": 1,
    "maximum": 3.5,
    "average": 2.25,
    "values": [1, 3.5],
}
```

## Empty input behavior

Empty or fully filtered input returns zero totals and nullable range metrics:

```python
summary = summarize_numbers([None, "skip", False])

assert summary["count"] == 0
assert summary["total"] == 0
assert summary["minimum"] is None
assert summary["maximum"] is None
assert summary["average"] is None
assert summary["values"] == []
```

## Design notes

The helper returns a plain dictionary rather than a class because the surrounding
spike already uses lightweight functions and simple assertions. A future product
version can replace this with a typed object if the API grows.

The `values` field is deliberately preserved. It gives reviewers and downstream
scripts a simple way to see which entries were accepted without recomputing the
filtering rules.

The boolean exclusion is deliberate. In Python:

```python
isinstance(True, int) == True
```

Counting `True` as `1` and `False` as `0` would make feature flags, validation
results, or parser booleans silently skew summaries. The helper avoids that
class of bug by filtering booleans before calculating metrics.

The finite-number check is also deliberate. A single `NaN` would otherwise
propagate through `sum`, `min`, `max`, and `average`, making every metric hard to
compare or serialize safely.
